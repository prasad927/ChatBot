from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass


@dataclass
class InteractionLog:
    """Log entry for each user interaction."""
    timestamp: str
    query: str
    response: str
    agent_steps: List[Dict]
    tools_used: List[str]
    feedback: Optional[str] = None
    feedback_timestamp: Optional[str] = None
