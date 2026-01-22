from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
import json


@dataclass
class TaskOutput:
    """
    Standardized output format for all task results.
    Wraps agent responses in consistent envelope.
    """
    task_id: str
    task_type: str
    status: str
    result: Dict[str, Any]
    confidence: Optional[str] = None
    duration_ms: Optional[int] = None

    @classmethod
    def from_result(cls, task_id: str, task_type: str, result: Dict[str, Any], 
                    duration_ms: Optional[int] = None):
        """
        Factory method: convert agent result to TaskOutput.
        Preserves original result in 'result' field.
        """
        status = result.get("status", "SUCCESS")
        confidence = result.get("confidence", None)
        
        return cls(
            task_id=task_id,
            task_type=task_type,
            status=status,
            result=result,
            confidence=confidence,
            duration_ms=duration_ms
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        return {k: v for k, v in asdict(self).items() if v is not None}

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2, default=str)
