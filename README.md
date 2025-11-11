To run this app first spin up a redis and then create a file in root folder named mini-judge.conf


It should look like
```conf
[REDIS]
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
QUEUE_NAME=mini_judge_queue
```