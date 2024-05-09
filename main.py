from queries import AsyncORM
import socketio
import uvicorn
from fastapi import FastAPI


app = FastAPI()
sio = socketio.AsyncServer(cors_allowed_origins='*', async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

connections = {}


@sio.on("init_user")
async def connection(sid, data):
    print(f"Сид конект {sid}")
    user_id = data.get("userID")
    connections[sid] = user_id
    user = await AsyncORM.get_user(user_id)
    print("ЭТо юзер", user)
    if user:
        ser_user = user.__dict__
        del ser_user["_sa_instance_state"]
        await sio.emit("get_user", ser_user)
    else:
        new_user = {
            "id": user_id,
            "balance": 0,
            "auto_miner": 0
        }
        await AsyncORM.insert_user(user_id)
        await sio.emit("get_user", new_user)


@sio.on("click")
async def handle_clicks(sid, data: dict):
    print(f'Сид при кликах {sid}')
    user_id = data.get("userID")
    clicks = data.get("clicks")
    await AsyncORM.update_balance(user_id, clicks)
    user = await AsyncORM.get_user(user_id)
    ser_user = user.__dict__
    del ser_user["_sa_instance_state"]
    await sio.emit("get_user", ser_user)


@sio.on("single_click")
async def handle_single(sid, user_id):
    """
    тут отправка на редис к юзеру по user_id
    """
    pass


@sio.on("disconnect")
async def disconnect(sid):
    if sid in connections.keys():
        print(f"Сид при дисконекте {sid}")



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)

