import redis
from exceptions import EmptyQueueException

class TaskQueue:
    QUEUE_KEY = "taskQueue"

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def push_task(self, task: str):
        self.redis.lpush(self.QUEUE_KEY, task)

    def get_next_task(self) -> str:
        task = self.redis.rpop(self.QUEUE_KEY)
        if task is None:
            raise EmptyQueueException("Task queue is empty.")
        return task
