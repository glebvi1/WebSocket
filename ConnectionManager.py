from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self):
        self.clients: dict[int, WebSocket] = {}
        self.id1: int = 1
        self.sim: Optional[WebSocket] = None

    async def connect_cli(self, websocket: WebSocket):
        self.clients[self.id1] = websocket
        print(f"Создал клиента №{self.id1}")

        await self.send_to_sim(f"{self.id1},new_connect")
        print(f"Клиент №{self.id1} подключился к симулятору")

        self.id1 += 1
        return self.id1 - 1

    async def disconnect(self, websocket: WebSocket):
        remove_id = 0
        for id, socket in self.clients.items():
            if socket == websocket:
                remove_id = id
                break
        self.clients.pop(remove_id)
        await self.send_to_sim(f"{remove_id},closed")
        print(f"Клиент {remove_id} отсоединился")

    async def send_to_sim(self, message: str):
        await self.sim.send_text(message)

    async def send_to_cli(self, client_id: int, message: str):
        await self.clients[client_id].send_text(message)
