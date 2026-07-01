from typing import Any


class MemoryManager:
    def __init__(self):
        self.memory: list[dict[str, Any]] = []

    def add_memory(self, tool_name: str, observation: Any):
        self.memory.append(
            {
                "tool": tool_name,
                "observation": observation,
            }
        )

    def get_memory(self):
        return self.memory

    def clear(self):
        self.memory.clear()


memory_manager = MemoryManager()
