from queries import AsyncORM
import socketio
import uvicorn
from fastapi import FastAPI
from redis import asyncio as aioredis


r = aioredis.Redis(host='redis', port=6379, decode_responses=True)
app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

connections = {}


@sio.on("init_user")
async def connection(sid, data):
    user_id = data.get("userID")
    connections[sid] = user_id
    user = await AsyncORM.get_user(user_id)
    if user:
        result = await r.set(user_id, user.balance, get=True)
        print(f"Результат вставки: {result}")
        ser_user = user.__dict__
        del ser_user["_sa_instance_state"]
        await sio.emit("get_user", ser_user)
    else:
        result = await r.set(user_id, 0, get=True)
        print(f"Результат вставки: {result}")
        new_user = {
            "id": user_id,
            "balance": 0,
            "auto_miner": 0
        }
        await AsyncORM.insert_user(user_id)
        await sio.emit("get_user", new_user)


@sio.on("click")
async def handle_clicks(sid, data: dict):
    user_id = data.get("userID")
    clicks = data.get("clicks")
    await AsyncORM.update_balance(user_id, clicks)
    user = await AsyncORM.get_user(user_id)
    ser_user = user.__dict__
    del ser_user["_sa_instance_state"]
    await sio.emit("get_user", ser_user)


@sio.on("single_click")
async def handle_single(sid, user_id):
    value = await r.get(user_id)
    print(f"Редис вернул {value}")
    await r.set(user_id, int(value) + 1)


@sio.on("disconnect")
async def disconnect(sid):
    print("Я в дисконект")
    if sid in connections.keys():
        print("Cид найден")
        curr_balance = int(await r.get(connections[sid]))
        user = await AsyncORM.get_user(connections[sid])
        if user.balance < curr_balance:
            await AsyncORM.update_balance(connections[sid], curr_balance - user.balance)
        await r.delete(connections[sid])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
