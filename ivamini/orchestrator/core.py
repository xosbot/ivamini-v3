from ivamini.agents.analysis_agent import AnalysisAgent
from ivamini.memory.session import SessionMemory
from ivamini.tasks.task import Task
from ivamini.models.output import TaskOutput
import time


def extract_depth(text: str) -> str:
    if "[DEPTH=HIGH]" in text:
        return "HIGH"
    return "LOW"


def has_execution_verbs(text: str) -> bool:
    """Check if text contains execution verbs (forbidden in PLAN mode)"""
    execution_verbs = [
        "run ", "execute ", "implement ", "build ", "start ", "begin ",
        "do ", "perform ", "conduct ", "trigger ", "launch ", "activate "
    ]
    text_lower = text.lower()
    return any(verb in text_lower for verb in execution_verbs)


def enforce_mode(task_type: str, content: str) -> str:
    if task_type == "QUESTION":
        return f"Provide a definition only.\n\n{content}"
    if task_type == "PLAN":
        return f"Provide a deterministic 7-part plan:\n1. Objective\n2. Assumptions\n3. Constraints\n4. Step-by-step plan\n5. Risks\n6. Validation checks\n7. What is NOT being done\n\n{content}"
    return content


class Orchestrator:
    """
    Central control layer.
    Owns permissions, memory, and agent coordination.
    """

    def __init__(self):
        self.analysis_agent = AnalysisAgent()
        self.session_memory = SessionMemory()

    def create_task(self, mode: str, task_type: str, content: str):
        """
        Create a canonical Task object.
        """
        return Task.create(
            mode=mode,
            task_type=task_type,
            content=content,
        )

    def execute_task(self, task: Task):
        start_time = time.time()

        # STATUS command
        if task.mode == "STATUS":
            result = {
                "status": "SUCCESS",
                "model": "llama3.2:1b",
                "context_length": 2048,
                "permissions": "READ",
                "memory_entries": len(self.session_memory.entries),
                "ollama": "CONNECTED",
                "session_started_at": self.session_memory.started_at,
            }
            duration_ms = int((time.time() - start_time) * 1000)
            return TaskOutput.from_result(task.task_id, task.mode, result, duration_ms).to_dict()

        # MEMORY inspection
        if task.mode == "MEMORY":
            result = {
                "status": "SUCCESS",
                "started_at": self.session_memory.started_at,
                "entries": self.session_memory.entries,
            }
            duration_ms = int((time.time() - start_time) * 1000)
            return TaskOutput.from_result(task.task_id, task.mode, result, duration_ms).to_dict()

        # Enforce mode semantics
        content = enforce_mode(task.task_type, task.content)

        # REVIEW / PLAN / QUESTION
        if task.task_type in ("REVIEW", "PLAN", "QUESTION"):
            depth = extract_depth(content)

            if task.task_type == "REVIEW":
                if depth == "HIGH":
                    prompt = (
                        "Provide a structured, multi-section risk analysis.\n\n"
                        + content
                    )
                else:
                    prompt = (
                        "Provide a concise, risk-focused summary.\n\n"
                        + content
                    )
            else:
                prompt = content

            # Inject session memory (read-only)
            session_context = self.session_memory.summarize()

            # PLAN mode uses special system prompt
            result = self.analysis_agent.run(
                prompt,
                session_context=session_context,
                task_type=task.task_type  # Pass task type to agent
            )

            # PLAN mode: read-only, no memory writes
            # REVIEW/QUESTION: write summary to memory
            if task.task_type != "PLAN" and result and "summary" in result:
                self.session_memory.add(
                    result["summary"],
                    kind=task.task_type
                )

            duration_ms = int((time.time() - start_time) * 1000)
            return TaskOutput.from_result(task.task_id, task.task_type, result, duration_ms).to_dict()

        # COMMAND fallback (no execution here)
        result = {
            "status": "NO_EXECUTION",
            "reason": "Command execution not enabled in this system"
        }
        duration_ms = int((time.time() - start_time) * 1000)
        return TaskOutput.from_result(task.task_id, task.mode, result, duration_ms).to_dict()
