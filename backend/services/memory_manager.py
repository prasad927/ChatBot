from backend.services.logger import logger
from backend.models.schemas import InteractionLog
from typing import List, Dict
from pathlib import Path
from datetime import datetime
import pickle


class MemoryManager:
    """Manages conversation memory and interaction history."""
    
    def __init__(self, memory_path: str = "memory_store_old"):

        """Initialize memory management system."""
        self.memory_path = Path(memory_path)
        self.memory_path.mkdir(exist_ok=True)
        
        # Long-term interaction history
        self.interaction_history: List[InteractionLog] = []
        
        # Load existing memory
        self._load_memory()
        
        logger.info("Memory Manager initialized")


    def add_interaction(self, query: str, response: str, agent_steps: List[Dict], tools_used: List[str]):

        """Add a new interaction to memory."""
        interaction = InteractionLog(
            timestamp=datetime.now().isoformat(),
            query=query,
            response=response,
            agent_steps=agent_steps,
            tools_used=tools_used
        )
        self.interaction_history.append(interaction)
        
        # Save after every interaction
        self._save_memory()
        
        logger.info(f"Interaction saved (total: {len(self.interaction_history)})")


    def add_feedback(self, interaction_index: int, feedback: str):

        """Add user feedback to a specific interaction."""
        if 0 <= interaction_index < len(self.interaction_history):
            self.interaction_history[interaction_index].feedback = feedback
            self.interaction_history[interaction_index].feedback_timestamp = datetime.now().isoformat()
            self._save_memory()
            logger.info(f"👍/👎 Feedback added to interaction {interaction_index}")

    
    def clear_memory(self):

        """Clear all interaction history."""
        self.interaction_history = []
        self._save_memory()
        logger.info("🗑️ All conversation history cleared")
    
    
    def _save_memory(self):

        """Save interaction history to disk."""
        history_file = self.memory_path / "interaction_history.pkl"
        with open(history_file, 'wb') as f:
            pickle.dump(self.interaction_history, f)
        logger.info(f"💾 Memory saved to {history_file}")
    

    def _load_memory(self):

        """Load interaction history from disk."""
        history_file = self.memory_path / "interaction_history.pkl"
        if history_file.exists():
            try:
                with open(history_file, 'rb') as f:
                    self.interaction_history = pickle.load(f)
                logger.info(f"📂 Loaded {len(self.interaction_history)} past interactions")
            except Exception as e:
                logger.warning(f"⚠️ Could not load memory: {e}")
