import asyncio
import websockets

import sys
sys.path.insert(0, "../")

from sockets import SIM_TYPE, URI


async def websocket_client(analyze):
    """Клиент зависит только от функции analyze(), которая должна принимать один строковый
    аргумент - ответ симулятора. Функция возвращает строку"""
    async with websockets.connect(URI) as websocket:
        while True:
            data = await asyncio.wait_for(websocket.recv(), timeout=10)
            if data == "who_r_u":
                await websocket.send("its_cli")
            else:
                data1 = analyze(data)
                await websocket.send(data1)


if __name__ == "__main__":
    if SIM_TYPE == "neuromorph":
        asyncio.run(websocket_client(lambda _: "0,0,0,0"))
    elif SIM_TYPE == "firefighter":
        from algorithm.PID import analyze
        asyncio.run(websocket_client(analyze))
