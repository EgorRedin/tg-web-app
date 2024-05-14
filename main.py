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
        await r.hset(str(user_id), mapping={"balance": user.balance, "click_size": user.click_size})
        ser_user = user.__dict__
        del ser_user["_sa_instance_state"]
        await sio.emit("get_user", ser_user, room=sid)
    else:
        await r.hset(str(user_id), mapping={"balance": 0, "click_size": 1})
        new_user = {
            "id": user_id,
            "balance": 0,
            "auto_miner": 0,
            "click_size": 1
        }
        await AsyncORM.insert_user(user_id)
        await sio.emit("get_user", new_user, room=sid)


@sio.on("click")
async def handle_clicks(sid, data: dict):
    user_id = data.get("userID")
    clicks = data.get("clicks")
    await AsyncORM.update_balance(user_id, clicks)
    user = await AsyncORM.get_user(user_id)
    ser_user = user.__dict__
    del ser_user["_sa_instance_state"]
    await sio.emit("get_user", ser_user, room=sid)


@sio.on("single_click")
async def handle_single(sid, data: dict):
    user_id = str(data.get("userID"))
    click_size = int(data.get("clickSize"))
    value = await r.hgetall(user_id)
    if click_size != value["click_size"]:
        user = await AsyncORM.get_user(int(user_id))
        value["click_size"] = user.click_size
        value["balance"] += value["click_size"]
        await r.hset(user_id, mapping=value)
    else:
        value["balance"] += value["click_size"]
        await r.hset(user_id, mapping=value)


@sio.on("update_click")
async def handle_size(sid, user_id):
    updated_user = await AsyncORM.update_click_size(user_id)
    ser_user = updated_user.__dict__
    del ser_user["_sa_instance_state"]
    await sio.emit("init_user", ser_user, room=sid)


@sio.on("disconnect")
async def disconnect(sid):
    if sid in connections.keys():
        curr_balance = int(await r.hgetall(str(connections[sid])))
        user = await AsyncORM.get_user(connections[sid])
        if user.balance < curr_balance:
            await AsyncORM.update_balance(connections[sid], curr_balance - user.balance)
        await r.delete(connections[sid])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
