import asyncio
import websockets


async def handler(websocket):
    while True:
        await websocket.send("risk_update")
        await asyncio.sleep(1)


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())