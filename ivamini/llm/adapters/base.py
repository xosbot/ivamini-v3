from abc import ABC, abstractmethod

class LLMAdapter(ABC):
    """
    Abstract Base Class for all LLM Providers.
    Ensures a consistent interface for the ModelRouter.
    """

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = None, **kwargs) -> str:
        """
        Send a prompt to the provider and return the text response.

        Args:
            prompt (str): The user's input prompt.
            system_prompt (str, optional): System instructions for behavior/persona.
            **kwargs: Additional provider-specific parameters (e.g., temperature).

        Returns:
            str: The raw text response from the model.
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is currently reachable/configured.

        Returns:
            bool: True if available, False otherwise.
        """
        pass
