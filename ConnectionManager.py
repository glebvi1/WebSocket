import logging

from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self):
        self.clients: dict[int, WebSocket] = {}
        self.id1: int = 1
        self.sim: Optional[WebSocket] = None

    def connect_sim(self, websocket: WebSocket):
        self.sim = websocket
        logging.info(f"Симулятор подключен: {websocket}")

    async def connect_cli(self, websocket: WebSocket):
        self.clients[self.id1] = websocket
        logging.debug(f"Создал клиента №{self.id1}")

        await self.send_to_sim(f"{self.id1},new_connect")
        logging.info(f"Клиент №{self.id1} подключился к симулятору")

        self.id1 += 1
        return self.id1 - 1

    async def disconnect(self, websocket: WebSocket):
        remove_id = -1
        for id, socket in self.clients.items():
            if socket == websocket:
                remove_id = id
                break
        if remove_id == -1:
            return
        self.clients.pop(remove_id)
        await self.send_to_sim(f"{remove_id},closed")
        logging.info(f"Клиент {remove_id} отсоединился")

    async def send_to_sim(self, message: str):
        if not self.sim:
            logging.critical(f"Не дошло до симулятора")
            return
        await self.sim.send_text(message)
        logging.debug(f"Отправленно симулятору: \"{message}\"")

    async def send_to_cli(self, client_id: int, message: str):
        if client_id not in self.clients:
            logging.debug(f"Не дошло до клиента №{client_id}: \"{message}\"")
            return
        await self.clients[client_id].send_text(message)
        logging.debug(f"Отправленно клиенту №{client_id}: \"{message}\"")
