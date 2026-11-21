
import os
import redis
from dotenv import load_dotenv

load_dotenv()

# Connect to Redis using environment variables
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", "6380")),
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
