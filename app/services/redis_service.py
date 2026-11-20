
import redis

# Connect to Redis running in Docker
redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True,
    protocol=2
)

def save_message(session_id: str, role: str, message: str) -> None:
    """
    Save a conversation message in Redis.
    """
    key = f"chat:{session_id}"

    redis_client.rpush(
        key,
        f"{role}: {message}"
    )


def get_chat_history(session_id: str) -> list[str]:
    """
    Retrieve conversation history from Redis.
    """
    key = f"chat:{session_id}"

    return redis_client.lrange(key, 0, -1)
