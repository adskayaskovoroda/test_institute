from dataclasses import dataclass
from collections import defaultdict


class Strategy:
    def do_work(self):
        # actual work here
        pass


class NoAvailableTasks(Exception):
    pass


@dataclass
class Resources:
    ram: int
    cpu_cores: int
    gpu_count: int

    def __ge__(self, other: 'Resources'):
        return self.ram >= other.ram and self.cpu_cores >= other.cpu_cores and self.gpu_count >= other.gpu_count

    def __le__(self, other: 'Resources'):
        return self.ram <= other.ram or self.cpu_cores <= other.cpu_cores or self.gpu_count <= other.gpu_count

    def __gt__(self, other):
        return self.ram > other.ram and self.cpu_cores > other.cpu_cores and self.gpu_count > other.gpu_count

    def __lt__(self, other):
        return self.ram < other.ram or self.cpu_cores < other.cpu_cores or self.gpu_count < other.gpu_count


@dataclass
class Task:
    id: int
    priority: int
    resources: Resources
    content: Strategy = None
    result: str = None


class TaskQueue:
    def __init__(self):
        self._queue = defaultdict(list)

    def add_task(self, task: Task):
        self._queue[task.priority].append(task)

    def get_task(self, available_resources: Resources) -> Task:
        for priority, queue in sorted(self._queue.items()):
            for index, task in enumerate(queue):
                if available_resources < task.resources:
                    continue

                del self._queue[priority][index]
                return task

        raise NoAvailableTasks('Task queue is empty or available resources are insufficient')
