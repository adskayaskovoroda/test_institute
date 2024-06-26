import pytest
from task_queue import Resources, Task, TaskQueue, NoAvailableTasks


class TestTaskQueue:
    def test_basic(self):
        queue = TaskQueue()
        resources = Resources(1, 1, 1)
        task = Task(0, 0, resources)

        queue.add_task(task)
        assert queue.get_task(resources) is task
        with pytest.raises(NoAvailableTasks):
            queue.get_task(resources)

    def test_priority(self):
        queue = TaskQueue()
        resources = Resources(1, 1, 1)
        task_1 = Task(0, 1, resources)
        task_2 = Task(1, 2, resources)
        task_3 = Task(2, 3, resources)

        queue.add_task(task_3)
        queue.add_task(task_1)
        queue.add_task(task_2)

        assert queue.get_task(resources) is task_1
        assert queue.get_task(resources) is task_2
        assert queue.get_task(resources) is task_3

    def test_resources(self):
        queue = TaskQueue()
        available_resources = Resources(ram=8000, cpu_cores=8, gpu_count=4)
        task_1 = Task(0, 1, Resources(ram=16000, cpu_cores=4, gpu_count=4))  # more ram
        task_2 = Task(1, 2, Resources(ram=4000, cpu_cores=4, gpu_count=8))  # more gpu_count
        task_3 = Task(2, 3, Resources(ram=6000, cpu_cores=6, gpu_count=2))  # less then available
        task_4 = Task(3, 4, Resources(ram=8000, cpu_cores=8, gpu_count=4))  # same as available

        queue.add_task(task_2)
        queue.add_task(task_4)
        queue.add_task(task_1)
        queue.add_task(task_3)

        assert queue.get_task(available_resources) is task_3
        assert queue.get_task(available_resources) is task_4
        with pytest.raises(NoAvailableTasks):
            queue.get_task(available_resources)

    def test_same_priority(self):
        queue = TaskQueue()
        resources = Resources(1, 1, 1)
        task_1 = Task(0, 1, resources)
        task_2 = Task(1, 1, resources)

        queue.add_task(task_1)
        queue.add_task(task_2)

        assert queue.get_task(resources) is task_1
        assert queue.get_task(resources) is task_2
