from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Task:
    task_id: str
    mode: str
    intent: str

    task_type: str = ""
    plan: List[str] = field(default_factory=list)
    permissions: Dict = field(default_factory=dict)
    status: str = "CREATED"
