from fastapi import FastAPI
from api import router

app = FastAPI()

app.include_router(router)

#######################
from fastapi import WebSocket
import asyncio

# 연결된 클라이언트 저장
clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)

    try:
        while True:

            # 🔥 핵심: SimulationCore 상태 계속 push
            state = core.get_state()

            await websocket.send_json(state)

            await asyncio.sleep(0.5)

    except:
        clients.remove(websocket)

from fastapi import WebSocket
import asyncio

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:

            state = core.get_state()

            await websocket.send_json(state)

            await asyncio.sleep(0.5)

    except:
        print("WebSocket disconnected")