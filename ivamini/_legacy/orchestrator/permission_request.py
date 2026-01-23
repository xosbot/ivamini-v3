from dataclasses import dataclass
from datetime import datetime

@dataclass
class PermissionRequest:
    task_id: str
    requested_level: str
    reason: str
    status: str = "PENDING"
    created_at: str = datetime.now().isoformat()
