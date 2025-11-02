
import os
import json
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import asdict

# LangChain imports - OLD STYLE (0.4.x)
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory

# Tool imports
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from backend.services.memory_manager import MemoryManager
from backend.services.tool_data_formater import DataFormatterTool
from backend.services.tool_document_search import DocumentSearchTool
from backend.services.tool_text_analysis import TextAnalysisTool
from backend.services.tool_python_calculator import PythonCalculatorTool
from backend.services.logger import logger
from backend.models.schemas import InteractionLog
from backend.config.settings import settings


# Tavily Search (replaces SerpAPI)
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("Tavily not available. Install: pip install tavily-python")


class AgenticRAG:
    """
    Agentic RAG System using initialize_agent method.
    
    Uses: AgentType.ZERO_SHOT_REACT_DESCRIPTION
    """

    def __init__(self, memory_path: str = "memory_store"):
        """Initialize the Agentic RAG System."""
        logger.info("🚀 Initializing Agentic RAG System with initialize_agent()...")
        
        # Core components
        self.llm = ChatOpenAI(model=settings.model_name, temperature=settings.temperature,api_key=settings.openai_api_key)
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore: Optional[FAISS] = None
        self.document_metadata: Dict[str, Any] = {}

        # Memory manager
        self.memory_manager = MemoryManager(memory_path)


        # Custom tool instances
        self.doc_search_tool = DocumentSearchTool()
        self.calculator_tool = PythonCalculatorTool()
        self.text_analysis_tool = TextAnalysisTool()
        self.data_formatter_tool = DataFormatterTool()

         # Conversation memory for agent (maintains context across tools)
        self.agent_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Agent (initialized with tools)
        self.agent_executor = None

        # Initialize agent with tools
        self._initialize_agent()

        # Load recent conversations into agent memory
        self._load_recent_conversations_to_memory()

        logger.info("Agentic RAG System initialized")


    def _load_recent_conversations_to_memory(self):
        """Load recent conversations from MemoryManager into agent memory."""
        # Get last 10 interactions
        recent = self.memory_manager.interaction_history[-10:]
        
        for interaction in recent:
            # Save to agent memory
            self.agent_memory.save_context(
                {"input": interaction.query},
                {"output": interaction.response}
            )
        
        if recent:
            logger.info(f"📚 Loaded {len(recent)} past conversations into agent memory")


    def _initialize_agent(self):
        """Initialize agent using OLD initialize_agent method."""
        logger.info("Initializing agent with initialize_agent()...")
        
        # Create tool list
        tools = self._create_tools()

        # Custom parsing error handler
        def handle_parsing_error(error) -> str:
            """Provide helpful feedback when agent has formatting errors."""
            return (
                "ERROR: Invalid format detected. You must use this EXACT format:\n\n"
                "Thought: [your reasoning]\n"
                "Action: [tool name]\n"
                "Action Input: [input for the tool]\n\n"
                "Example:\n"
                "Thought: The user asks about the document, so I should search it.\n"
                "Action: DocumentSearch\n"
                "Action Input: databases\n\n"
                "If you cannot use tools, use DirectAnswer to respond directly."
            )
        
        # OLD WAY: Using initialize_agent with AgentType and Memory
        # Using CONVERSATIONAL_REACT_DESCRIPTION which properly uses conversation memory
        try:
            self.agent_executor = initialize_agent(
                tools=tools,
                llm=self.llm,
                agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # Changed from ZERO_SHOT
                verbose=True,
                memory=self.agent_memory,  # Conversation memory for context
                handle_parsing_errors=handle_parsing_error,
                max_iterations=6,
                early_stopping_method="generate",
                return_intermediate_steps=True
            )
            logger.info(f"Agent initialized with {len(tools)} tools + memory (CONVERSATIONAL agent)")
        except Exception as e:
            logger.error(f"Failed to initialize agent: {e}")
            raise

    
    def _create_tools(self) -> List[Tool]:
        """Create all available tools for the agent."""
        tools = []
        
        # 0. Direct Answer Tool - DEFAULT for most questions (agent has conversation memory)
        tools.append(
            Tool(
                name="DirectAnswer",
                func=lambda query: self.llm.invoke(query).content,
                description="""Answer questions directly using LLM knowledge (DEFAULT tool for most questions).
Use for: facts, concepts, explanations, logic, reasoning, general knowledge, comparisons, definitions.
The agent has conversation memory, so you can reference previous messages with "it", "its", "that".
Examples: "What is cloud computing?", "Explain Azure vs AWS", "its population" (referring to previous topic).
ALWAYS use this UNLESS user needs: document search, calculations, or explicitly says "latest/today/now/2025"."""
            )
        )
        
        # 1. Document Search Tool - ONLY for uploaded PDF
        tools.append(
            Tool(
                name="DocumentSearch",
                func=self.doc_search_tool.search,
                description="""Search the uploaded PDF document ONLY when user explicitly mentions the document.
Trigger phrases: "in the document", "from the PDF", "according to the file", "what does the document say".
Input: Search keywords (e.g., "databases", "Azure Storage").
Example: "What databases are mentioned IN THE DOCUMENT?" → input: "databases".
For general questions, use DirectAnswer instead."""
            )
        )
        
        # 2. Calculator Tool - ONLY for math
        tools.append(
            Tool(
                name="Calculator",
                func=self.calculator_tool.calculate,
                description="""Perform mathematical calculations.
Use when: User asks to calculate, compute, or do math.
Input: Math expression ONLY (e.g., "25*4", "100/12", "2+2").
Example: "Calculate 25 times 4" → input: "25*4"."""
            )
        )
        
        # 3. Text Analysis Tool - ONLY when explicitly requested
        tools.append(
            Tool(
                name="TextAnalysis",
                func=self.text_analysis_tool.analyze,
                description="""Analyze text to get word count, keywords, and summary.
Use when: User explicitly asks to ANALYZE text.
Input: The text to analyze.
Example: "Analyze this: [text]" → input: "[text]"."""
            )
        )
        
        # 4. Data Formatter Tool - ONLY when explicitly requested
        tools.append(
            Tool(
                name="DataFormatter",
                func=self.data_formatter_tool.format,
                description="""Format items as a bullet point list.
Use when: User explicitly asks to FORMAT or make a LIST.
Input: Comma-separated items.
Example: "List these as bullets: A, B, C" → input: "A, B, C"."""
            )
        )
        
        # 5. Web Search Tool - ONLY when user explicitly asks for real-time info
        if TAVILY_AVAILABLE and len (settings.tavily_api_key) !=0:
            try:
                # TavilySearchResults is already a BaseTool, use directly
                tavily_tool = TavilySearchResults(
                    max_results=3,
                    name="WebSearch",
                    description="""Search internet ONLY when user EXPLICITLY says: "latest", "today", "now", "2024", "2025", "current", "recent".
DO NOT use for general questions - use DirectAnswer instead.
Input: Search query.
Example: "Latest Azure pricing TODAY" → input: "Azure pricing 2024"."""
                )
                tools.append(tavily_tool)
                logger.info("Tavily WebSearch tool added")
            except Exception as e:
                logger.warning(f"Tavily tool failed to initialize: {e}")
        else:
            logger.info("Tavily WebSearch not available (set TAVILY_API_KEY to enable)")
        
        # 6. Wikipedia Tool - ONLY when explicitly needed (rarely use)
        # WikipediaQueryRun is already a BaseTool, but we need to set the name
        wikipedia_tool = WikipediaQueryRun(
            api_wrapper=WikipediaAPIWrapper(),
            name="Wikipedia",
            description="""Search Wikipedia ONLY when DirectAnswer cannot help with very specific factual topics.
RARELY use this - prefer DirectAnswer for most questions.
Use ONLY if user explicitly says "Wikipedia" or needs very specific biographical/historical facts.
Input: Search topic.
Example: User says "Check Wikipedia for..." → input: search term."""
        )
        tools.append(wikipedia_tool)
        
        logger.info(f"Created {len(tools)} tools: {[t.name for t in tools]}")
        return tools
    


    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF document and create vector database.
        Same as main version.
        """
        try:
            logger.info(f"Processing PDF: {pdf_path}")
            
            # Load PDF
            loader = PyPDFLoader(pdf_path)
            pages = loader.load()
            
            if not pages:
                return {
                    'success': False,
                    'error': 'No content extracted from PDF'
            }
            
            # Split into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200,
                separators=["\n\n", "\n", " ", ""]
            )
            chunks = text_splitter.split_documents(pages)
            
            # Create vector store
            self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
            
            # Update document search tool
            self.doc_search_tool.update_vectorstore(self.vectorstore)
            
            # Save to disk
            self.vectorstore.save_local("faiss_index")
            
            # Store metadata
            self.document_metadata = {
                'filename': Path(pdf_path).name,
                'pages': len(pages),
                'chunks': len(chunks),
                'timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"PDF processed: {len(pages)} pages, {len(chunks)} chunks")
            
            return {
                'success': True,
                'filename': self.document_metadata['filename'],
                'pages': len(pages),
                'chunks': len(chunks)
            }
            
        except Exception as e:
            logger.error(f"PDF processing failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
        
    
    def chat(self, query: str) -> Dict[str, Any]:
        """
        Main chat interface using OLD initialize_agent.
        
        Args:
            query: User's question
            
        Returns:
            Dict with response and metadata
        """
        if not self.agent_executor:
            return {
                "response": "Agent not initialized properly.",
                "metadata": {"error": "Agent initialization failed"}
            }
        
        try:
            logger.info(f"Processing query: {query[:100]}...")
            
            # OLD WAY: invoke with {"input": query}
            result = self.agent_executor.invoke({"input": query})
            
            # Debug logging
            logger.info(f"Result keys: {result.keys()}")
            logger.info(f"Intermediate steps count: {len(result.get('intermediate_steps', []))}")
            
            # Extract response (OLD format)
            response = result.get('output', 'No response generated')
            
            # Extract intermediate steps (tools used)
            intermediate_steps = result.get('intermediate_steps', [])
            tools_used = []
            agent_steps = []
            
            for i, step in enumerate(intermediate_steps):
                logger.info(f"📝 Step {i+1}: {type(step)}, length: {len(step) if isinstance(step, (list, tuple)) else 'N/A'}")
                if len(step) >= 2:
                    action, observation = step[0], step[1]
                    tool_name = action.tool if hasattr(action, 'tool') else 'Unknown'
                    tool_input = action.tool_input if hasattr(action, 'tool_input') else ''
                    
                    logger.info(f"🔧 Tool: {tool_name}, Input: {str(tool_input)[:50]}")
                    
                    if tool_name not in tools_used:
                        tools_used.append(tool_name)
                    
                    agent_steps.append({
                        'tool': tool_name,
                        'input': str(tool_input)[:100],
                        'output': str(observation)[:200] + '...' if len(str(observation)) > 200 else str(observation)
                    })
            
            logger.info(f"Extracted {len(agent_steps)} agent steps")
            logger.info(f"Tools used: {tools_used}")
            
            # Save to memory
            self.memory_manager.add_interaction(
                query=query,
                response=response,
                agent_steps=agent_steps,
                tools_used=tools_used
            )
            
            # Format response
            result_dict = {
                "response": response,
                "metadata": {
                    "tools_used": tools_used,
                    "num_steps": len(agent_steps),
                    "agent_reasoning": agent_steps
                },
                "conversation_id": len(self.memory_manager.interaction_history) - 1
            }
            
            logger.info(f"Query completed. Tools used: {tools_used}")
            return result_dict
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            import traceback
            traceback.print_exc()
            return {
                "response": f"An error occurred: {str(e)}",
                "metadata": {"error": str(e)}
            }
    

    def add_feedback(self, conversation_id: int, feedback: str):
        """Add user feedback to a conversation."""
        self.memory_manager.add_feedback(conversation_id, feedback)
    

    def get_conversation_history(self, num_interactions: int = 10) -> List[InteractionLog]:
        """Get recent conversation history."""
        return self.memory_manager.interaction_history[-num_interactions:]
    

    def clear_memory(self):
        """Clear conversation memory."""
        self.memory_manager.clear_memory()
        # Also clear agent's conversation memory
        self.agent_memory.clear()
        logger.info("Memory cleared from UI (both MemoryManager and agent memory)")
    

    def export_logs(self, filepath: str = "interaction_logs.json") -> bool:
        """Export interaction logs to JSON."""
        try:
            logs = [asdict(log) for log in self.memory_manager.interaction_history]
            with open(filepath, 'w') as f:
                json.dump(logs, f, indent=2)
            logger.info(f"Logs exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export logs: {e}")
            return False
    