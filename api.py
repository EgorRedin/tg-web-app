from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import jsons
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

async def db_click(tg_id):
    con=db_conn()
    await con.execute ('''INSERT into balance WHERE tg_id={tg_id} VALUES {$1}''',1) 

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/click/{tg_id}/ws")
async def websocket_endpoint_click(websocket: WebSocket,tg_id:str):
    await websocket.accept()
    db_tg_id=tg_id
    while True:
        print('1')
        data = await websocket.receive_text()
        if data=='1':
            await db_click(db_tg_id)
            await websocket.send_text(f"Message text was: {data}")
        #elif data==' ' todo next handlers