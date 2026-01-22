from datetime import datetime

class SessionMemory:
    """
    Volatile, in-memory store.
    Lives only for the current runtime.
    """

    def __init__(self):
        self.started_at = datetime.utcnow().isoformat()
        self.entries = []

    def add(self, content: str, kind: str = "NOTE"):
        self.entries.append({
            "time": datetime.utcnow().isoformat(),
            "type": kind,
            "content": content
        })

    def summarize(self) -> str:
        if not self.entries:
            return ""

        lines = []
        for e in self.entries[-5:]:  # keep last 5 only
            lines.append(f"- ({e['type']}) {e['content']}")

        return "Session context:\n" + "\n".join(lines)
