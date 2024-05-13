from queries import AsyncORM
import asyncio

if __name__ == "__main__":
    asyncio.run(AsyncORM.create_table())
