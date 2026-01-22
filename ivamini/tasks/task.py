from dataclasses import dataclass
import uuid


@dataclass
class Task:
    """
    Canonical task object passed through the system.
    """
    task_id: str
    mode: str
    task_type: str
    content: str

    @classmethod
    def create(cls, mode: str, task_type: str, content: str):
        return cls(
            task_id=str(uuid.uuid4())[:8],
            mode=mode,
            task_type=task_type,
            content=content,
        )
