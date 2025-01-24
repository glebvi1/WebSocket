import logging
import time
from tests import PATH_TEST
import json

from fastapi import WebSocket
from typing import Optional


class ConnectionManager:
    def __init__(self, is_debug=False):
        """
        В ключах self.times будет храниться id клиента, которое соответствует id в self.clients.
        В значениях - список из пар:
        1 значение - время ожидание ответа от симулятора
        2 значение - время ожидание ответа от клиента
        """
        self.clients: dict[int, WebSocket] = {}
        self.id1 = 1
        self.sim: Optional[WebSocket] = None

        self.is_debug = is_debug
        if is_debug:
            self.times: dict[int, list[list[float, float]]] = {}

    def connect_sim(self, websocket: WebSocket):
        self.sim = websocket
        logging.info(f"Симулятор подключен: {websocket}")

    async def connect_cli(self, websocket: WebSocket):
        self.clients[self.id1] = websocket
        logging.debug(f"Создал клиента №{self.id1}")

        if self.is_debug:
            self.times[self.id1] = []
            logging.debug(f"Создан список для хранения времени клиента №{self.id1}")

        await self.send_to_sim(self.id1, f"{self.id1},new_connect")
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

        if self.is_debug and len(self.clients) == 0:
            self.save_to_file()

        await self.send_to_sim(remove_id, f"{remove_id},closed")
        logging.info(f"Клиент №{remove_id} отсоединился")

    async def send_to_sim(self, client_id: int, message: str):
        self.answer_from_cli(client_id)

        if not self.sim:
            logging.critical(f"Не дошло до симулятора от клиента №{client_id}")
            return

        if self.is_debug:
            self.times[client_id].append([])
            self.times[client_id][-1].append(time.time())

        await self.sim.send_text(message)
        logging.debug(f"Отправленно симулятору: \"{message}\" от клиента №{client_id}")

    def answer_from_sim(self, client_id: int):
        if not self.is_debug:
            return
        self.times[client_id][-1][0] = round(time.time() - self.times[client_id][-1][0], 5)

    def answer_from_cli(self, client_id: int):
        if not self.is_debug or len(self.times[client_id]) == 0:
            return
        self.times[client_id][-1][1] = round(time.time() - self.times[client_id][-1][1], 5)

    async def send_to_cli(self, client_id: int, message: str):
        self.answer_from_sim(client_id)

        if client_id not in self.clients:
            logging.debug(f"Не дошло до клиента №{client_id}: \"{message}\"")
            return

        if self.is_debug:
            self.times[client_id][-1].append(time.time())

        await self.clients[client_id].send_text(message)
        logging.debug(f"Отправленно клиенту №{client_id}: \"{message}\"")

    def save_to_file(self):
        with open(PATH_TEST + "time2.json", "w") as fp:
            json.dump(self.times, fp)
