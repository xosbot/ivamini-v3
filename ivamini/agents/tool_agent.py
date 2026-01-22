from ivamini.tools.registry import ToolRegistry
from ivamini.orchestrator.permissions import is_allowed

class ToolAgent:

    def run(self, tool_name: str, task_permission: str, tool_input=None):
        tool = ToolRegistry.get(tool_name)

        if not tool:
            return "ERROR: Tool not found"

        if not is_allowed(task_permission, tool.permission):
            return f"BLOCKED: Permission {task_permission} cannot access {tool.permission} tool"

        if tool_input is not None:
            return tool.execute(tool_input)

        return tool.execute()
