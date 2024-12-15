import asyncio
import websockets

URI = "ws://localhost:41235/"


async def websocket_client():
    async with websockets.connect(URI) as websocket:
        while True:
            data = await asyncio.wait_for(websocket.recv(), timeout=10)
            if data == "who_r_u":
                await websocket.send("its_cli")
            else:
                # формально, на основе данных с сервера (data), клиент
                # их как-то анализирует и создает data1
                data1 = "step,1"
                print(f"Клиент получил:", data)
                await websocket.send(data1)


if __name__ == "__main__":
    asyncio.run(websocket_client())
