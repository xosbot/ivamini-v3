class EchoAgent:
    def run(self, text: str) -> str:
        if not text:
            return "ERROR: No input provided"

        return f"ECHO: {text}"
