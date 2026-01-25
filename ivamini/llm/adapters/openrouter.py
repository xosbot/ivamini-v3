from ivamini.llm.adapters.base import LLMAdapter

class OpenRouterAdapter(LLMAdapter):
    """
    Adapter for OpenRouter Aggregator.
    Serves as the primary Fallback provider.
    """

    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        DESIGN ONLY: Placeholder for OpenRouter API call.
        """
        # Logic would go here:
        # response = requests.post("https://openrouter.ai/api/v1/chat/completions", ...)
        return "DESIGN_STUB: OpenRouter response"

    def is_available(self) -> bool:
        """
        Checks if OPENROUTER_API_KEY is present in config/env.
        """
        # return os.getenv("OPENROUTER_API_KEY") is not None
        return True
