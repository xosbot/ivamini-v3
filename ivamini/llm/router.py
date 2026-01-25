from ivamini.llm.adapters.gemini import GeminiAdapter
from ivamini.llm.adapters.groq import GroqAdapter
from ivamini.llm.adapters.openrouter import OpenRouterAdapter

class ModelRouter:
    """
    Central Routing Layer for IVA-Cortex v1.0.
    Determines the best provider based on task mode and system state.
    """

    def __init__(self):
        # Initialize providers
        self.gemini = GeminiAdapter()
        self.groq = GroqAdapter()
        self.openrouter = OpenRouterAdapter()

    def route(self, mode: str, prompt: str, metadata: dict = None) -> str:
        """
        Routes the request to the appropriate provider.

        Routing Rules:
        1. PLAN / REVIEW -> Gemini (High reasoning)
        2. QUESTION (short) -> Groq (Low latency)
        3. Fallback -> OpenRouter (if primary unavailable)

        Args:
            mode (str): Task mode (PLAN, REVIEW, QUESTION, etc.)
            prompt (str): The prompt content.
            metadata (dict, optional): Additional context (e.g., depth).

        Returns:
            str: The generated text response.
        """
        if metadata is None:
            metadata = {}

        # Rule 1: High Reasoning Tasks
        if mode in ["PLAN", "REVIEW"]:
            if self.gemini.is_available():
                return self.gemini.generate(prompt)
            else:
                # Fallback
                return self.openrouter.generate(prompt)

        # Rule 2: Low Latency Tasks
        if mode == "QUESTION":
            # Simple heuristic for "short" question (e.g., < 100 chars) could go here
            # For now, default all QUESTIONs to Groq as per design
            if self.groq.is_available():
                return self.groq.generate(prompt)
            else:
                # Fallback
                return self.openrouter.generate(prompt)

        # Default / Other Modes
        # Prefer capability (Gemini) over speed for unknown tasks
        if self.gemini.is_available():
            return self.gemini.generate(prompt)

        return self.openrouter.generate(prompt)
