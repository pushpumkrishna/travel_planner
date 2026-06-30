from typing import List


class MemoryManager:

    def __init__(self):
        self.memory: List[dict] = []

    def add_memory(self, tool_name: str, observation: str):

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


# Singleton
memory_manager = MemoryManager()
