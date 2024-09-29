import redis

# 初始化 Redis 连接
redis_client = redis.StrictRedis(host='1.15.7.2', port=6372, db=0)

def consumer():
    while True:
        # 从 Redis 队列中获取消息（阻塞式）
        message = redis_client.brpop('task_queue')
        print(f"Consumed message: {message[1].decode('utf-8')}")
consumer()