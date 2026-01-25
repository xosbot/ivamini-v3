from ivamini.llm.router import ModelRouter
from ivamini.llm.interface import SYSTEM_PROMPT, PLAN_SYSTEM_PROMPT
from ivamini.memory.facts import load_facts


class AnalysisAgent:
    """
    Uses ModelRouter for reasoning.
    No execution, no tools, no memory writes.
    """

    def __init__(self):
        # REPLACE: LocalLLM with ModelRouter
        self.router = ModelRouter()
        self.facts = load_facts()

    def run(self, content: str, session_context: str = "", task_type: str = "QUESTION"):
        """
        Run analysis with optional session context injection.
        Uses PLAN_SYSTEM_PROMPT for PLAN mode, standard SYSTEM_PROMPT otherwise.
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

        # Use appropriate system prompt based on task type
        system_prompt = PLAN_SYSTEM_PROMPT if task_type == "PLAN" else SYSTEM_PROMPT
        
        # REPLACE: self.llm.analyze -> self.router.route
        return self.router.route(
            mode=task_type,
            prompt=content,
            system_prompt=system_prompt
        )
