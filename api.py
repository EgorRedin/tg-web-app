from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import json
from bd12 import queries
from bd12 import configurable_doc
import asyncpg
app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
async def db_conn():
    con = await asyncpg.connect(user='postgres',host='localhost',port='5432',database='postgres',password='postgres')
    return con 

async def db_click(tg_id,count,time):
    con=db_conn()
    cur=con.cursor()
    if count//time<14.1:
        await cur.execute ('''INSERT into balance WHERE tg_id={tg_id} VALUES {$1}''',1)

async def db_get_data(tg_id):
    conn=db_conn()
    cur=conn.cursor()
    await cur.execute("SELECT balance, automainer  WHERE tg_id=%s ", ( tg_id ) )
    db = cur.fetchone()
    print ( db )
    return db        

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/click/{tg_id}/ws")
async def websocket_endpoint_click(websocket: WebSocket,tg_id:str):
    await websocket.accept()
    db_tg_id=tg_id
    while True:
        print('1')
        data = await websocket.receive()#recive_text
        if data["handler"]=='1':
            await db_click(db_tg_id,data["count"],data["time"])
            db = await db_get_data(tg_id)
            user_balance = db[0]
            automainer = db[1]
            await websocket.send(json.stringfy(tg_id,user_balance,automainer))#send text
        #elif data==' ' todo next handlers