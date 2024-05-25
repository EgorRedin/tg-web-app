from datetime import datetime, timezone
from queries import AsyncORM
import socketio
import uvicorn
from fastapi import FastAPI
from redis import asyncio as aioredis
import logging

r = aioredis.Redis(host='redis', port=6379, decode_responses=True)
app = FastAPI()
logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)
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
        if ser_user["auto_miner"] > 0:
            logger.debug(f"С БД {ser_user["last_enter"]}\nСервер: {datetime.now(timezone.utc)}")
            time_gap = int((datetime.now(timezone.utc).replace(tzinfo=None) - ser_user["last_enter"]).total_seconds())
            coins_left = ser_user["auto_miner"] - time_gap if ser_user["auto_miner"] - time_gap > 0 else 0
            if time_gap > 60:
                await AsyncORM.update_auto_miner(user_id, coins_left)
                await AsyncORM.update_balance(user_id, ser_user["auto_miner"] - coins_left)
                ser_user["balance"] += (ser_user["auto_miner"] - coins_left)
        del ser_user["_sa_instance_state"]
        del ser_user["last_enter"]
        await sio.emit("get_user", ser_user, to=sid)
    else:
        await r.hset(str(user_id), mapping={"balance": 0, "click_size": 1})
        new_user = {
            "id": user_id,
            "balance": 0,
            "auto_miner": 0,
            "click_size": 1,
        }
        await AsyncORM.insert_user(user_id)
        await sio.emit("get_user", new_user, to=sid)


@sio.on("click")
async def handle_clicks(sid, data: dict):
    user_id = data.get("userID")
    clicks = data.get("clicks")
    user = await AsyncORM.get_user(user_id)
    if (clicks / user.click_size) / 10 < 14.1:
        await AsyncORM.update_balance(user_id, clicks)
        user.balance += clicks
    ser_user = user.__dict__
    del ser_user["last_enter"]
    del ser_user["_sa_instance_state"]
    await sio.emit("get_user", ser_user, to=sid)


@sio.on("single_click")
async def handle_single(sid, data: dict):
    user_id = str(data.get("userID"))
    auto_miner = data.get("autoMiner")
    click_size = int(data.get("clickSize"))
    values = await r.hgetall(user_id)
    values = {key: int(value) for key, value in values.items()}
    if auto_miner:
        values["balance"] += 1
        await r.hset(user_id, mapping=values)
        return
    if click_size != values["click_size"]:
        user = await AsyncORM.get_user(int(user_id))
        values["click_size"] = user.click_size
        values["balance"] += values["click_size"]
        await r.hset(user_id, mapping=values)
    else:
        values["balance"] += values["click_size"]
        await r.hset(user_id, mapping=values)


@sio.on("update_click")
async def handle_size(sid, user_id):
    await AsyncORM.update_click_size(user_id)
    updated_user = await AsyncORM.get_user(user_id)
    ser_user = updated_user.__dict__
    del ser_user["last_enter"]
    del ser_user["_sa_instance_state"]
    await sio.emit("get_user", ser_user, to=sid)


@sio.on("update_auto_miner")
async def handel_auto_miner(sid, user_id):
    user = await AsyncORM.get_user(user_id)
    if user.auto_miner > 0:
        return
    await AsyncORM.update_auto_miner(user_id, 360)


@sio.on("disconnect")
async def disconnect(sid):
    if sid in connections.keys():
        curr_balance = int((await r.hgetall(str(connections[sid])))["balance"])
        user = await AsyncORM.get_user(connections[sid])
        await AsyncORM.update_last_enter(connections[sid])
        if user.balance < curr_balance:
            await AsyncORM.update_balance(connections[sid], curr_balance - user.balance)
        await r.delete(str(connections[sid]))
        del connections[sid]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80, log_level="debug")
