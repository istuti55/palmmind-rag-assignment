
from app.services.redis_service import (
    redis_client,
    save_message,
    get_chat_history
)

# Check Redis connection
print("Redis connected:", redis_client.ping())

# Save two messages
save_message("test_session", "user", "What is FastAPI?")
save_message("test_session", "assistant", "FastAPI is a Python framework.")

# Retrieve conversation history
history = get_chat_history("test_session")

print("\nConversation history:")
for message in history:
    print(message)
