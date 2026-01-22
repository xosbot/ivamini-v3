class MemoryCandidateAgent:
    def evaluate(self, content: str):
        """
        Evaluate whether something deserves memory.
        This agent NEVER stores memory.
        """

        if len(content) < 10:
            return {
                "store": False,
                "reason": "Too trivial"
            }

        return {
            "store": True,
            "type": "FACT",
            "confidence": "MEDIUM",
            "reason": "User query with informational value"
        }
