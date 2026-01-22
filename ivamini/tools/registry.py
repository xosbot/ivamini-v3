class ToolRegistry:
    _tools = {}

    @classmethod
    def register(cls, name, tool):
        cls._tools[name] = tool

    @classmethod
    def get(cls, name):
        return cls._tools.get(name)

    @classmethod
    def list_tools(cls):
        return list(cls._tools.keys())
