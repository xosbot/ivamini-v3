from ivamini.llm.interface import LocalLLM
from ivamini.memory.facts import load_facts


class AnalysisAgent:
    """
    Uses LLM ONLY for reasoning.
    No execution, no tools, no memory writes.
    """

    def __init__(self):
        self.llm = LocalLLM()
        self.facts = load_facts()

    def run(self, content: str, session_context: str = ""):
        """
        Run analysis with optional session context injection.
        """

        # Inject session context (read-only)
        if session_context:
            content = session_context + "\n\nUser request:\n" + content

        # Inject known facts (read-only)
        injected_facts = []
        for key, value in self.facts.items():
            if key.lower() in content.lower():
                injected_facts.append(f"{key}: {value}")

        if injected_facts:
            content = (
                "Known facts:\n"
                + "\n".join(injected_facts)
                + "\n\n"
                + content
            )

        return self.llm.analyze(content)
