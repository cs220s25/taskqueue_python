import argparse
import redis
from task_queue import TaskQueue
from exceptions import EmptyQueueException

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Task Queue CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add a task to the queue")
    add_parser.add_argument("task", type=str, help="Task description")

    subparsers.add_parser("next", help="Retrieve the next task")

    args = parser.parse_args()

    try:
        redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)
        redis_client.ping()
        queue = TaskQueue(redis_client)

        if args.command == "add":
            queue.push_task(args.task)
            print(f"Task added: {args.task}")
        elif args.command == "next":
            try:
                print(f"Next task: {queue.get_next_task()}")
            except EmptyQueueException:
                print("No tasks in the queue.")
    except redis.ConnectionError:
        print("Error: Unable to connect to Redis. Ensure the Redis server is running on localhost:6379.")
