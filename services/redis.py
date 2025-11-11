from redis import Redis
from rq import Queue

from utils.config import mini_judge_config


redis_conn = Redis(host=mini_judge_config["REDIS_HOST"],port=mini_judge_config["REDIS_PORT"])


class RedisQueue:
    def __init__(self, queue_name: str, redis_conn: Redis):
        self.queue: Queue = Queue(queue_name, connection=redis_conn)
        self.redis_conn: Redis = redis_conn

    def getQueue(self) -> Queue:
        return self.queue