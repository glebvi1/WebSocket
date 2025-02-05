import asyncio
from client import websocket_client


def default_analyze(data):
    return "1,step"


async def run_3clients():
    """
    1) Запускаю 3х клиентов
    2) Откл 3его
    3) Подключаю 3его
    4) Откл 3его, 2ого
    """
    clients = [asyncio.create_task(websocket_client(default_analyze)) for _ in range(3)]

    await asyncio.sleep(5)
    clients[2].cancel()
    print("Откл 3")

    await asyncio.sleep(5)
    clients.append(asyncio.create_task(websocket_client(default_analyze)))
    print("Добавил")

    await asyncio.sleep(5)
    clients[2].cancel()
    print("Откл 4")
    await asyncio.sleep(5)
    clients[1].cancel()
    print("Откл 2")
    await asyncio.sleep(5)
    clients[0].cancel()
    print("Откл все")


async def run_30clients():
    clients = [asyncio.create_task(websocket_client(default_analyze)) for _ in range(30)]
    await asyncio.sleep(60*5)

    print("Отключаем...")

    for client in clients:
        client.cancel()
        await asyncio.sleep(5)


async def run_30clients2():
    clients = [asyncio.create_task(websocket_client(default_analyze)) for _ in range(30)]
    await asyncio.sleep(60 * 5)
    [client.cancel() for client in clients]


if __name__ == "__main__":
    asyncio.run(run_30clients2())
