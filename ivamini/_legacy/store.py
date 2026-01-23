from ivamini.models.task import Task
from ivamini.agents.echo_agent import EchoAgent
from ivamini.agents.tool_agent import ToolAgent
from ivamini.agents.memory_candidate_agent import MemoryCandidateAgent
from ivamini.logs.logger import log_event
from ivamini.orchestrator.permission_manager import PermissionManager
import uuid


class Orchestrator:

    def __init__(self):
        self.permission_manager = PermissionManager()

    def create_task(self, mode: str, intent: str) -> Task:
        task = Task(
            task_id=str(uuid.uuid4())[:8],
            mode=mode,
            intent=intent
        )

        task.task_type = self.classify_task(task)
        task.plan = self.generate_plan(task)
        task.permissions = self.assign_permissions(task)
        task.status = "PLANNED"

        log_event("TASK_CREATED", {
            "task_id": task.task_id,
            "mode": task.mode,
            "type": task.task_type,
            "intent": task.intent
        })

        return task

    def classify_task(self, task: Task) -> str:
        if task.mode == "PLAN":
            return "PLANNING"
        elif task.mode == "COMMAND":
            return "EXECUTION"
        elif task.mode == "QUESTION":
            return "QUERY"
        elif task.mode == "REVIEW":
            return "REVIEW"
        else:
            return "UNKNOWN"

    def generate_plan(self, task: Task):
        if task.task_type == "PLANNING":
            return [
                "Clarify objective",
                "Identify required information",
                "Assess risks"
            ]
        return []

    def assign_permissions(self, task: Task):
        # Default permission
        return {
            "level": "READ"
        }

    def execute_task(self, task):
        result = None

        if task.task_type == "QUERY":
            agent = EchoAgent()
            result = agent.run(task.intent)

            mem_agent = MemoryCandidateAgent()
            memory_eval = mem_agent.evaluate(task.intent)

            log_event("MEMORY_CANDIDATE", {
                "task_id": task.task_id,
                "evaluation": memory_eval
            })

        elif task.task_type == "EXECUTION" and task.intent.startswith("search:"):
            agent = ToolAgent()
            result = agent.run("web_search", task.permissions["level"],
                               task.intent.replace("search:", "").strip())

        elif task.task_type == "EXECUTION" and task.intent == "delete_all":
            # 🚨 Escalation required
            req = self.permission_manager.request_permission(
                task.task_id,
                "DESTRUCTIVE",
                "User requested delete_all operation"
            )
            result = f"PERMISSION REQUIRED: {req}"

        elif task.task_type == "EXECUTION" and task.intent == "get_time":
            agent = ToolAgent()
            result = agent.run("get_time", task.permissions["level"])

        else:
            result = "No execution required"

        log_event("TASK_EXECUTED", {
            "task_id": task.task_id,
            "result": result
        })

        return result
