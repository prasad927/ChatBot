# -*- coding: utf-8 -*-
"""
Interactive UI for Agentic RAG System
=========================================

Gradio-based user interface with:
- File upload
- Interactive chat
- Memory trace visualization
- Feedback collection
- Agent reasoning display

Author: Agentic RAG UI
Version: 3.0 - Enhanced Dynamic UI
"""
import os
import sys
import gradio as gr
from typing import List, Tuple, Dict
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.services.agentic_rag import AgenticRAG


CUSTOM_CSS = """
/* Global Styles */
.gradio-container {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header Styling */
.app-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    color: white;
    box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
}

.app-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.app-header p {
    font-size: 1.1rem;
    opacity: 0.95;
}

/* Status Cards */
.status-card {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Success Status */
.status-success {
    border-left-color: #10b981;
    background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

/* Error Status */
.status-error {
    border-left-color: #ef4444;
    background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
}

/* Reasoning Panel */
.reasoning-panel {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #f59e0b;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Sources Panel */
.sources-panel {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #3b82f6;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* Stats Cards */
.stats-card {
    background: white;
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 1rem 0;
    border-top: 3px solid #667eea;
    transition: transform 0.2s ease;
}

.stats-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* Metric Display */
.metric {
    display: inline-block;
    padding: 0.5rem 1rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    font-weight: 600;
    margin: 0.25rem;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

/* Buttons Enhancement */
.primary-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.75rem 2rem !important;
    border-radius: 8px !important;
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4) !important;
    transition: all 0.3s ease !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
}

/* Chatbot Styling */
.chatbot-container {
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Loading Animation */
.loading {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 3px solid rgba(102, 126, 234, 0.3);
    border-radius: 50%;
    border-top-color: #667eea;
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Badge Styles */
.badge {
    display: inline-block;
    padding: 0.25rem 0.75rem;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.25rem;
}

.badge-success {
    background: #10b981;
    color: white;
}

.badge-warning {
    background: #f59e0b;
    color: white;
}

.badge-info {
    background: #3b82f6;
    color: white;
}

/* Feedback Buttons */
.feedback-btn {
    font-size: 1.5rem;
    padding: 0.5rem 1.5rem;
    border-radius: 8px;
    transition: all 0.2s ease;
}

.feedback-btn:hover {
    transform: scale(1.1);
}

/* Progress Bar */
.progress-bar {
    width: 100%;
    height: 4px;
    background: #e5e7eb;
    border-radius: 2px;
    overflow: hidden;
    margin: 1rem 0;
}

.progress-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    animation: progress 2s ease-in-out infinite;
}

@keyframes progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
}

/* Tab Styling */
.tab-nav button {
    font-weight: 600;
    font-size: 1rem;
    padding: 1rem 1.5rem;
    border-radius: 8px 8px 0 0;
    transition: all 0.2s ease;
}

.tab-nav button.selected {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

/* Pulse Animation */
@keyframes pulse {
    0%, 100% {
        opacity: 1;
    }
    50% {
        opacity: 0.7;
    }
}

.pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
"""

# ═══════════════════════════════════════════════════════════════════
# Global System Instance
# ═══════════════════════════════════════════════════════════════════

rag_system = AgenticRAG()

# ═══════════════════════════════════════════════════════════════════
# UI Handler Functions
# ═══════════════════════════════════════════════════════════════════

def load_conversation_history() -> Tuple[List[Tuple[str, str]], str]:
    """Load past conversation history when UI starts."""
    try:
        history = rag_system.get_conversation_history(num_interactions=50)
        
        if not history:
            return [], """
            <div class="status-card status-info">
                <h3>💬 New Session</h3>
                <p>No previous conversations found. Start a new conversation!</p>
            </div>
            """
        
        # Convert to Gradio chatbot format
        chat_history = []
        for interaction in history:
            chat_history.append((interaction.query, interaction.response))
        
        status_msg = f"""
        <div class="status-card status-success">
            <h3>📂 Conversation History Loaded</h3>
            <p>✅ Restored <strong>{len(history)}</strong> previous conversations</p>
            <p style="font-size: 0.9em; opacity: 0.8; margin-top: 0.5rem;">
                Last conversation: {history[-1].timestamp if history else 'N/A'}
            </p>
            <p style="font-size: 0.85em; margin-top: 1rem;">
                💡 <strong>Tip:</strong> Your conversations are automatically saved. You can continue where you left off!
            </p>
        </div>
        """
        
        return chat_history, status_msg
        
    except Exception as e:
        return [], f"""
        <div class="status-card status-warning">
            <h3>⚠️ Could Not Load History</h3>
            <p>Error: {str(e)}</p>
            <p>Starting fresh session...</p>
        </div>
        """

def process_pdf_ui(pdf_file) -> str:
    """Process uploaded PDF file with enhanced visual feedback."""
    if not pdf_file:
        return """
        <div class="status-card status-error">
            <h3>⚠️ No File Selected</h3>
            <p>Please upload a PDF file to continue.</p>
        </div>
        """
    
    result = rag_system.process_pdf(pdf_file.name)
    
    if result['success']:
        return f"""
        <div class="status-card status-success">
            <h2>✅ Document Processed Successfully!</h2>
            <div style="margin-top: 1rem;">
                <div class="metric">📄 {result['filename']}</div>
                <div class="metric">📑 {result['pages']} pages</div>
                <div class="metric">📊 {result['chunks']} chunks</div>
            </div>
            <p style="margin-top: 1rem; font-size: 1.1rem;">
                <strong>🤖 Status:</strong> Ready to answer your questions!
            </p>
            <p style="margin-top: 0.5rem; color: #059669;">
                ⚡ Vector embeddings created • Document indexed • Ready for semantic search
            </p>
        </div>
        """
    else:
        error_msg = result.get('error', 'Unknown error')
        return f"""
        <div class="status-card status-error">
            <h3>❌ Processing Failed</h3>
            <p><strong>Error:</strong> {error_msg}</p>
            <p style="margin-top: 0.5rem;">
                💡 <em>Tip: Make sure the PDF is text-based and not corrupted.</em>
            </p>
        </div>
        """


def chat_ui(message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], Dict]:
    """Handle chat interaction."""
    if not message.strip():
        return history, {}
    
    # Get response from system
    result = rag_system.chat(message)
    
    # Extract response and metadata
    response = result.get('response', 'No response generated')
    metadata = result.get('metadata', {})
    
    # IMPORTANT: Include conversation_id in metadata for feedback
    if 'conversation_id' in result:
        metadata['conversation_id'] = result['conversation_id']
    
    # Add to history
    history.append((message, response))
    
    return history, metadata


def display_agent_reasoning(metadata: Dict) -> str:
    """Format agent reasoning with enhanced visuals - TRUE AGENTIC VERSION."""
    if not metadata:
        return """
        <div class="reasoning-panel">
            <h3>🤖 Agent Reasoning (ReAct Pattern)</h3>
            <p><em>Agent will autonomously decide which tools to use...</em></p>
        </div>
        """
    
    output = '<div class="reasoning-panel">'
    output += '<h2 style="margin-bottom: 1rem;">🤖 Agent Reasoning Process (ReAct)</h2>'
    
    # Tools Used Summary
    tools_used = metadata.get('tools_used', [])
    num_steps = metadata.get('num_steps', 0)
    
    output += '<div style="margin-bottom: 1.5rem; padding: 1rem; background: white; border-radius: 8px;">'
    output += '<h3>🛠️ Autonomous Tool Selection</h3>'
    output += f'<p><span class="badge badge-success">{len(tools_used)} tools used</span> '
    output += f'<span class="badge badge-info">{num_steps} reasoning steps</span></p>'
    
    if tools_used:
        output += '<p><strong>Tools:</strong> '
        tool_icons = {
            'DocumentSearch': '📚',
            'WebSearch': '🌐',
            'TavilySearch': '🔍',
            'Wikipedia': '📖',
            'Calculator': '🧮',
            'TextAnalysis': '📝',
            'DataFormatter': '📊'
        }
        for tool in tools_used:
            icon = tool_icons.get(tool, '🔧')
            output += f'<span class="badge" style="background: #667eea; color: white; margin: 0.25rem;">{icon} {tool}</span> '
        output += '</p>'
    output += '</div>'
    
    # Agent Steps (Thought → Action → Observation)
    agent_reasoning = metadata.get('agent_reasoning', [])
    if agent_reasoning:
        output += '<div style="margin-bottom: 1.5rem;">'
        output += '<h3>🧠 Agent\'s Thought Process</h3>'
        output += '<p><em>The agent uses ReAct (Reasoning + Acting) pattern</em></p>'
        
        for i, step in enumerate(agent_reasoning, 1):
            tool = step.get('tool', 'Unknown')
            tool_input = step.get('input', '')
            tool_output = step.get('output', '')
            
            output += f'<div style="margin: 1rem 0; padding: 1rem; background: #f9fafb; border-left: 4px solid #667eea; border-radius: 6px;">'
            output += f'<h4 style="color: #667eea; margin-bottom: 0.5rem;">Step {i}: {tool}</h4>'
            output += f'<p><strong>🎯 Action Input:</strong> <code>{tool_input}</code></p>'
            output += f'<p><strong>📋 Observation:</strong></p>'
            output += f'<div style="padding: 0.5rem; background: white; border-radius: 4px; font-family: monospace; font-size: 0.9rem; max-height: 150px; overflow-y: auto;">{tool_output}</div>'
            output += '</div>'
        
        output += '</div>'
    
    output += '</div>'
    return output


def display_sources(metadata: Dict) -> str:
    """Format tool outputs and agent observations."""
    if not metadata:
        return """
        <div class="sources-panel">
            <h3>📊 Agent Observations</h3>
            <p><em>Tool outputs and observations will appear here...</em></p>
        </div>
        """
    
    agent_reasoning = metadata.get('agent_reasoning', [])
    
    if not agent_reasoning:
        return """
        <div class="sources-panel">
            <h3>📊 Agent Observations</h3>
            <p>No tool outputs for this query.</p>
        </div>
        """
    
    output = '<div class="sources-panel">'
    output += f'<h2 style="margin-bottom: 1rem;">📊 Tool Outputs & Observations</h2>'
    
    for i, step in enumerate(agent_reasoning, 1):
        tool = step.get('tool', 'Unknown')
        tool_output = step.get('output', '')
        
        # Tool-specific icons
        tool_icons = {
            'DocumentSearch': '📚',
            'WebSearch': '🌐',
            'Wikipedia': '📖',
            'Calculator': '🧮',
            'TavilySearch': '🔍'
        }
        icon = tool_icons.get(tool, '🔧')
        
        output += f'<div style="margin-bottom: 1.5rem; padding: 1rem; background: white; border-radius: 8px;">'
        output += f'<h4 style="color: #3b82f6;">{icon} {tool}</h4>'
        output += f'<div style="margin-top: 0.5rem; padding: 0.75rem; background: #f9fafb; border-radius: 6px; font-size: 0.9rem; max-height: 200px; overflow-y: auto;">'
        output += f'{tool_output}'
        output += '</div></div>'
    
    output += '</div>'
    return output


def handle_feedback(conversation_id: int, feedback_type: str):
    """Handle user feedback with visual confirmation."""
    if conversation_id is not None and conversation_id >= 0:
        rag_system.add_feedback(conversation_id, feedback_type)
        emoji = "👍" if feedback_type == "positive" else "👎"
        color = "#10b981" if feedback_type == "positive" else "#ef4444"
        return f"""
        <div style="padding: 1rem; background: {color}20; border-radius: 8px; border-left: 4px solid {color};">
            <strong style="color: {color};">{emoji} Feedback Recorded!</strong>
            <p style="margin-top: 0.5rem;">Thank you for helping improve the system.</p>
        </div>
        """
    return """
    <div style="padding: 1rem; background: #fef3c7; border-radius: 8px; border-left: 4px solid #f59e0b;">
        <strong style="color: #f59e0b;">⚠️ No Active Conversation</strong>
        <p style="margin-top: 0.5rem;">Please ask a question first before providing feedback.</p>
    </div>
    """


def export_logs_ui():
    """Export interaction logs with confirmation."""
    success = rag_system.export_logs("interaction_logs.json")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if success:
        return f"""
        <div class="status-card status-success">
            <h4>✅ Logs Exported Successfully</h4>
            <p><strong>File:</strong> interaction_logs.json</p>
            <p><strong>Time:</strong> {timestamp}</p>
        </div>
        """
    return """
    <div class="status-card status-error">
        <h4>❌ Export Failed</h4>
        <p>Unable to export logs. Please check permissions.</p>
    </div>
    """


def clear_memory_ui():
    """Clear conversation memory with confirmation."""
    rag_system.clear_memory()
    return """
    <div class="status-card">
        <h4>🗑️ Memory Cleared</h4>
        <p>Conversation history has been reset. Starting fresh!</p>
    </div>
    """


def get_conversation_stats() -> str:
    """Get conversation statistics with enhanced visuals."""
    history = rag_system.get_conversation_history(num_interactions=100)
    
    if not history:
        return """
        <div class="stats-card">
            <h3>📊 Conversation Statistics</h3>
            <p><em>No conversations yet. Start chatting to see statistics!</em></p>
        </div>
        """
    
    total = len(history)
    with_feedback = sum(1 for h in history if h.feedback)
    positive = sum(1 for h in history if h.feedback == 'positive')
    negative = sum(1 for h in history if h.feedback == 'negative')
    
    # Calculate tool usage statistics
    all_tools = []
    for h in history:
        all_tools.extend(h.tools_used)
    
    from collections import Counter
    tool_counts = Counter(all_tools)
    most_used_tool = tool_counts.most_common(1)[0] if tool_counts else ("None", 0)
    
    # Satisfaction rate
    satisfaction_rate = (positive / with_feedback * 100) if with_feedback > 0 else 0
    
    output = '<div class="stats-card">'
    output += '<h2 style="margin-bottom: 1.5rem;">📊 Conversation Statistics</h2>'
    
    # Main metrics
    output += '<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1.5rem;">'
    
    output += f'''
    <div style="padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 8px; color: white; text-align: center;">
        <div style="font-size: 2rem; font-weight: bold;">{total}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Total Interactions</div>
    </div>
    '''
    
    output += f'''
    <div style="padding: 1rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 8px; color: white; text-align: center;">
        <div style="font-size: 2rem; font-weight: bold;">{positive}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">👍 Positive</div>
    </div>
    '''
    
    output += f'''
    <div style="padding: 1rem; background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); border-radius: 8px; color: white; text-align: center;">
        <div style="font-size: 2rem; font-weight: bold;">{len(tool_counts)}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">🛠️ Tools Used</div>
    </div>
    '''
    
    output += f'''
    <div style="padding: 1rem; background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); border-radius: 8px; color: white; text-align: center;">
        <div style="font-size: 2rem; font-weight: bold;">{satisfaction_rate:.0f}%</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Satisfaction Rate</div>
    </div>
    '''
    
    output += '</div>'
    
    # Tool Usage Breakdown
    output += '<div style="margin-top: 1.5rem; padding: 1rem; background: #f9fafb; border-radius: 8px;">'
    output += '<h3 style="margin-bottom: 1rem;">🛠️ Tool Usage Statistics</h3>'
    output += '<ul style="list-style: none; padding: 0;">'
    for tool, count in tool_counts.most_common():
        output += f'<li style="padding: 0.5rem;">🔧 <strong>{tool}:</strong> {count} times</li>'
    output += '</ul>'
    output += '</div>'
    
    # Detailed breakdown
    output += '<div style="margin-top: 1.5rem; padding: 1rem; background: #f9fafb; border-radius: 8px;">'
    output += '<h3 style="margin-bottom: 1rem;">📈 Detailed Breakdown</h3>'
    output += '<ul style="list-style: none; padding: 0;">'
    output += f'<li style="padding: 0.5rem;">💬 <strong>Total Interactions:</strong> {total}</li>'
    output += f'<li style="padding: 0.5rem;">📝 <strong>With Feedback:</strong> {with_feedback}</li>'
    output += f'<li style="padding: 0.5rem;">👍 <strong>Positive Feedback:</strong> {positive}</li>'
    output += f'<li style="padding: 0.5rem;">👎 <strong>Negative Feedback:</strong> {negative}</li>'
    output += f'<li style="padding: 0.5rem;">🛠️ <strong>Most Used Tool:</strong> {most_used_tool[0]} ({most_used_tool[1]}x)</li>'
    output += '</ul>'
    output += '</div>'
    
    output += '</div>'
    return output


def get_live_system_status():
    """Get live system status."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    return f"""
    <div style="padding: 1rem; background: linear-gradient(135deg, #10b981 0%, #059669 100%); border-radius: 8px; color: white;">
        <h4 style="margin: 0;">🟢 System Status: <strong>ONLINE</strong></h4>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
            Last updated: {timestamp}
        </p>
    </div>
    """


# ═══════════════════════════════════════════════════════════════════
# 🎨 Gradio Interface
# ═══════════════════════════════════════════════════════════════════

def create_ui():
    """Create the enhanced Gradio interface."""
    
    # Custom theme
    theme = gr.themes.Soft(
        primary_hue="purple",
        secondary_hue="blue",
        neutral_hue="slate",
        font=["Inter", "sans-serif"]
    ).set(
        button_primary_background_fill="*primary_500",
        button_primary_background_fill_hover="*primary_600",
    )
    
    with gr.Blocks(theme=theme, css=CUSTOM_CSS, title="🤖 Interactive Agentic RAG") as demo:
        
        # Enhanced Header
        gr.HTML("""
        <div class="app-header">
            <h1>🤖 Interactive Agentic RAG System</h1>
            <p>An intelligent conversational AI that thinks, retrieves, and reasons about your documents using advanced agent-based architecture.</p>
            <div style="margin-top: 1rem;">
                <span class="badge" style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;">
                    🧠 Agent-based Reasoning
                </span>
                <span class="badge" style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;">
                    💭 Conversational Memory
                </span>
                <span class="badge" style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;">
                    🎯 Self-Reflection
                </span>
                <span class="badge" style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem;">
                    📊 Quality Assurance
                </span>
            </div>
        </div>
        """)
        
        # System Status
        with gr.Row():
            system_status = gr.HTML(value=get_live_system_status())
        
        # Document Upload Section
        with gr.Tab("📄 Document Upload"):
            gr.Markdown("## 📤 Upload and Process Your PDF Document")
            gr.Markdown("Upload any PDF document to enable intelligent Q&A with semantic search and agent-based reasoning.")
            
            with gr.Row():
                with gr.Column(scale=2):
                    pdf_input = gr.File(
                        label="📂 Select PDF File",
                        file_types=[".pdf"],
                        file_count="single"
                    )
                with gr.Column(scale=1):
                    process_btn = gr.Button(
                        "🔄 Process Document",
                        variant="primary",
                        size="lg",
                        elem_classes=["primary-btn"]
                    )
            
            status_output = gr.HTML(label="Processing Status")
            
            gr.Markdown("""
            ### 💡 Tips for Best Results
            - Ensure your PDF contains selectable text (not scanned images)
            - Larger documents may take longer to process
            - The system will create vector embeddings for semantic search
            """)
            
            process_btn.click(
                fn=process_pdf_ui,
                inputs=[pdf_input],
                outputs=[status_output]
            )
        
        # Chat Section
        with gr.Tab("💬 Interactive Chat"):
            gr.Markdown("## 💬 Chat with Your Documents")
            gr.Markdown("Ask questions and watch the AI agent think through its reasoning process in real-time.")
            
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(
                        label="🤖 Conversation",
                        height=500,
                        show_copy_button=True,
                        bubble_full_width=False,
                        avatar_images=(None, "🤖"),
                        elem_classes=["chatbot-container"]
                    )
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            label="💭 Your Question",
                            placeholder="Ask anything about your document... (e.g., 'What is the main topic?', 'Summarize the key findings')",
                            lines=2,
                            scale=5,
                            autofocus=True
                        )
                        send_btn = gr.Button("📤 Send", variant="primary", scale=1, elem_classes=["primary-btn"])
                    
                    # Quick action buttons
                    with gr.Row():
                        clear_btn = gr.Button("🗑️ Clear Chat", size="sm", variant="secondary")
                        export_btn = gr.Button("📥 Export Logs", size="sm", variant="secondary")
                        load_history_btn = gr.Button("📂 Load History", size="sm", variant="primary")
                        refresh_btn = gr.Button("🔄 Refresh Stats", size="sm", variant="secondary")
                    
                    # Hidden state
                    conv_id_state = gr.State(value=-1)
                    metadata_state = gr.State(value={})
                    
                    # Feedback section
                    gr.Markdown("### 📊 Rate the Response")
                    with gr.Row():
                        thumbs_up = gr.Button("👍 Helpful", size="lg", elem_classes=["feedback-btn"])
                        thumbs_down = gr.Button("👎 Not Helpful", size="lg", elem_classes=["feedback-btn"])
                    
                    feedback_status = gr.HTML()
                
                with gr.Column(scale=2):
                    # Agent Reasoning Display
                    gr.Markdown("### 🤖 Live Agent Reasoning")
                    reasoning_output = gr.HTML(
                        value=display_agent_reasoning({}),
                        label="Reasoning Process"
                    )
                    
                    # Sources Display
                    gr.Markdown("### 📚 Retrieved Sources")
                    sources_output = gr.HTML(
                        value=display_sources({}),
                        label="Document Sources"
                    )
            
            # Example questions
            gr.Markdown("""
            ### 💡 Example Questions to Try
            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem;">
                <span class="badge badge-info">What is this document about?</span>
                <span class="badge badge-info">Summarize the key points</span>
                <span class="badge badge-info">What methodology was used?</span>
                <span class="badge badge-info">Compare different approaches</span>
                <span class="badge badge-info">What are the conclusions?</span>
            </div>
            """)
            
            # Chat interaction
            def chat_wrapper(message, history):
                new_history, metadata = chat_ui(message, history)
                reasoning = display_agent_reasoning(metadata)
                sources = display_sources(metadata)
                conv_id = metadata.get('conversation_id', -1)
                status = get_live_system_status()
                return new_history, reasoning, sources, conv_id, metadata, status
            
            send_btn.click(
                fn=chat_wrapper,
                inputs=[msg, chatbot],
                outputs=[chatbot, reasoning_output, sources_output, conv_id_state, metadata_state, system_status]
            ).then(
                lambda: "",
                outputs=[msg]
            )
            
            msg.submit(
                fn=chat_wrapper,
                inputs=[msg, chatbot],
                outputs=[chatbot, reasoning_output, sources_output, conv_id_state, metadata_state, system_status]
            ).then(
                lambda: "",
                outputs=[msg]
            )
            
            # Feedback buttons
            thumbs_up.click(
                fn=lambda conv_id: handle_feedback(conv_id, 'positive'),
                inputs=[conv_id_state],
                outputs=[feedback_status]
            )
            
            thumbs_down.click(
                fn=lambda conv_id: handle_feedback(conv_id, 'negative'),
                inputs=[conv_id_state],
                outputs=[feedback_status]
            )
            
            # Utility buttons
            clear_btn.click(
                fn=lambda: ([], clear_memory_ui(), "", ""),
                outputs=[chatbot, feedback_status, reasoning_output, sources_output]
            )
            
            export_btn.click(
                fn=export_logs_ui,
                outputs=[feedback_status]
            )
            
            load_history_btn.click(
                fn=load_conversation_history,
                outputs=[chatbot, feedback_status]
            )
            
            refresh_btn.click(
                fn=get_live_system_status,
                outputs=[system_status]
            )
        
        # Statistics Tab
        with gr.Tab("📊 Statistics & Analytics"):
            gr.Markdown("## 📈 System Statistics and Performance Analytics")
            gr.Markdown("Real-time insights into conversation quality, user satisfaction, and system performance.")
            
            with gr.Row():
                stats_btn = gr.Button("🔄 Refresh Statistics", variant="primary", size="lg", elem_classes=["primary-btn"])
                auto_refresh = gr.Checkbox(label="🔄 Auto-refresh every 10s", value=False)
            
            stats_output = gr.HTML(value=get_conversation_stats())
            
            stats_btn.click(
                fn=get_conversation_stats,
                outputs=[stats_output]
            )
            
            gr.Markdown("""
            ### 🧠 Memory System Architecture
            <div style="padding: 1.5rem; background: #f9fafb; border-radius: 12px; margin-top: 1rem;">
                <h4>How the System Remembers</h4>
                <ul>
                    <li><strong>🔄 Short-term Memory:</strong> Maintains recent conversation context (last 3 turns)</li>
                    <li><strong>💾 Long-term Memory:</strong> All past interactions stored in vector database</li>
                    <li><strong>🎯 Semantic Memory:</strong> Similar past conversations retrieved for context</li>
                    <li><strong>👍👎 Feedback Memory:</strong> User ratings stored for continuous improvement</li>
                </ul>
            </div>
            """)
        
        # Help Tab
        with gr.Tab("❓ Help & Guide"):
            gr.Markdown("""
            ## 🎯 Complete User Guide
            
            ### 🚀 Quick Start (3 Steps)
            
            <div style="display: grid; gap: 1rem; margin: 1.5rem 0;">
                <div class="stats-card">
                    <h3>1️⃣ Upload Your Document</h3>
                    <p>Go to the <strong>Document Upload</strong> tab, select a PDF file, and click <strong>Process Document</strong>. Wait for the success confirmation.</p>
                </div>
                
                <div class="stats-card">
                    <h3>2️⃣ Start Chatting</h3>
                    <p>Navigate to <strong>Interactive Chat</strong>, type your question, and watch the AI agent reason through its response in real-time.</p>
                </div>
                
                <div class="stats-card">
                    <h3>3️⃣ Provide Feedback</h3>
                    <p>Use the 👍 or 👎 buttons to rate responses, helping the system learn and improve over time.</p>
                </div>
            </div>
            
            ### 💾 Conversation Persistence
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>✅ Auto-Save Feature</h4>
                <p><strong>Your conversations are automatically saved!</strong> When you restart the system:</p>
                <ul>
                    <li>✅ Previous conversations are <strong>automatically loaded</strong> when you open the UI</li>
                    <li>✅ Click <strong>"📂 Load History"</strong> button to manually reload at any time</li>
                    <li>✅ All interactions are saved to disk every 5 messages</li>
                    <li>✅ Continue where you left off - no data loss!</li>
                </ul>
                <p style="margin-top: 1rem;"><em>💡 Tip: The system loads the last 50 conversations automatically. Use "🗑️ Clear Chat" to start fresh if needed.</em></p>
            </div>
            
            ### 🤖 Understanding the Agent Loop
            
            The system uses a 5-phase agent reasoning process:
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>1. PLAN 📋</h4>
                <p>Analyzes your question type, determines optimal retrieval strategy, and plans step-by-step execution.</p>
            </div>
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>2. RETRIEVE 🔍</h4>
                <p>Searches the vector database using semantic similarity, retrieves relevant passages, and ranks by relevance.</p>
            </div>
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>3. REASON 💡</h4>
                <p>Analyzes retrieved information, considers conversation context, reviews similar past interactions, and draws evidence-based conclusions.</p>
            </div>
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>4. RESPOND 💬</h4>
                <p>Generates comprehensive answer, shows reasoning process, indicates confidence level, and cites sources.</p>
            </div>
            
            <div style="padding: 1.5rem; background: linear-gradient(135deg, #fce7f3 0%, #fbcfe8 100%); border-radius: 12px; margin: 1rem 0;">
                <h4>5. REFLECT 🎯</h4>
                <p>Self-evaluates response quality (1-10 score), identifies potential issues, suggests improvements, and approves or flags for review.</p>
            </div>
            
            ### 💡 Pro Tips for Best Results
            
            - **Be Specific:** Clear, detailed questions get better answers
            - **Use Context:** Reference previous responses for follow-up questions
            - **Try Different Angles:** Rephrase complex questions if needed
            - **Provide Feedback:** Help the system learn your preferences
            - **Check Sources:** Review retrieved passages for verification
            - **Monitor Quality:** Watch the self-reflection scores
            
            ### 🔧 Advanced Features
            
            - **Multi-turn Conversations:** Maintains context across questions
            - **Semantic Search:** Finds relevant info by meaning, not just keywords
            - **Quality Assurance:** Every response is self-evaluated
            - **Transparent Reasoning:** See exactly how the agent thinks
            - **Feedback Loop:** System learns from your ratings
            - **Export Capability:** Download all interactions for analysis
            
            ### 🆘 Troubleshooting
            
            - **Slow Response:** Large documents take longer to process
            - **No Sources Found:** Try rephrasing your question
            - **Low Quality Score:** The AI detected potential issues - review carefully
            - **Connection Error:** Check your API key and internet connection
            """)
        
        # Footer
        gr.Markdown("""
        ---
        <div style="text-align: center; padding: 1rem; color: #6b7280;">
            <p><strong>🤖 Interactive Agentic RAG System v3.0</strong></p>
            <p>Built with LangChain • FAISS • OpenAI • Gradio</p>
            <p><em>Powered by Advanced Agent-Based Reasoning</em></p>
        </div>
        """)
        
        # Auto-load conversation history when the interface loads
        demo.load(
            fn=load_conversation_history,
            outputs=[chatbot, feedback_status]
        )
    
    return demo



# Launch with enhanced settings
if __name__ == "__main__":
    demo = create_ui()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7819,
        share=False,
        show_error=True,
        inbrowser=True
    )
