
from backend.services.logger import logger
from typing import List, Dict, Tuple, Optional, Any

# LangChain imports - OLD STYLE (0.4.x)
from langchain.agents import initialize_agent, AgentType
from langchain_core.tools import Tool
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain.memory import ConversationBufferMemory

# Tool imports
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from backend.services.memory_manager import MemoryManager
from backend.services.tool_data_formater import DataFormatterTool
from backend.services.tool_document_search import DocumentSearchTool
from backend.services.tool_text_analysis import TextAnalysisTool
from backend.services.tool_python_calculator import PythonCalculatorTool


# Tavily Search (replaces SerpAPI)
try:
    from langchain_community.tools.tavily_search import TavilySearchResults
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False
    print("⚠️  Tavily not available. Install: pip install tavily-python")


class AgenticRAG:
    """
    Agentic RAG System using initialize_agent method.
    
    Uses: AgentType.ZERO_SHOT_REACT_DESCRIPTION
    """

    def __init__(self, memory_path: str = "memory_store"):
        """Initialize the Agentic RAG System."""
        logger.info("🚀 Initializing Agentic RAG System with initialize_agent()...")
        
        # Core components
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
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

        logger.info("Agentic RAG System initialized")
    