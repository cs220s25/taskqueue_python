import pytest
import fakeredis
from task_queue import TaskQueue
from exceptions import EmptyQueueException

@pytest.fixture
def task_queue():
    fake_redis = fakeredis.FakeRedis(decode_responses=True)
    return TaskQueue(fake_redis)

def test_get_next_task_raises_exception_on_empty_queue(task_queue):
    with pytest.raises(EmptyQueueException, match="Task queue is empty."):
        task_queue.get_next_task()

def test_push_and_retrieve_task(task_queue):
    task_queue.push_task("Test Task")
    assert task_queue.get_next_task() == "Test Task"

def test_tasks_returned_in_order(task_queue):
    task_queue.push_task("Task 1")
    task_queue.push_task("Task 2")
    task_queue.push_task("Task 3")

    assert task_queue.get_next_task() == "Task 1"
    assert task_queue.get_next_task() == "Task 2"
    assert task_queue.get_next_task() == "Task 3"
