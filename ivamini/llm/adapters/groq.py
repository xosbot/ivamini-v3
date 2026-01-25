from ivamini.llm.adapters.base import LLMAdapter

class GroqAdapter(LLMAdapter):
    """
    Adapter for Groq LPU Inference.
    Optimized for low-latency tasks (e.g., definitions, quick questions).
    """

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        DESIGN ONLY: Placeholder for Groq API call.
        """
        # Logic would go here:
        # client = Groq(api_key=...)
        # chat_completion = client.chat.completions.create(...)
        return "DESIGN_STUB: Groq response"

    def is_available(self) -> bool:
        """
        Checks if GROQ_API_KEY is present in config/env.
        """
        # return os.getenv("GROQ_API_KEY") is not None
        return True
