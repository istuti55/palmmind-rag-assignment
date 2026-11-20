from app.database.db import engine

try:
    with engine.connect() as connection:
        print("PostgreSQL connected successfully!")
except Exception as error:
    print("Database connection failed:", error)