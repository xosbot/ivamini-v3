PERMISSION_LEVELS = {
    "READ": 1,
    "WRITE": 2,
    "EXECUTE": 3,
    "DESTRUCTIVE": 4
}
def is_allowed(task_permission: str, tool_permission: str) -> bool:
    return PERMISSION_LEVELS[task_permission] >= PERMISSION_LEVELS[tool_permission]
