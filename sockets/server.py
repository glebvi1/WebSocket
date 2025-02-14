import logging
import sys
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

sys.path.insert(0, "../")

from algorithm.PID import analyze

app = FastAPI()


@app.websocket("/")
async def websocket_sim(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("who_r_u")
        answer = await websocket.receive_text()

        if answer != "its_sim":
            return

        logging.info(f"Симулятор подключен: {websocket}")
        await websocket.send_text("1,new_connect")  # ?

        while True:
            data = await websocket.receive_text()
            logging.debug(f"Данные с симулятора: {data}")

            new_data = analyze(data)
            logging.debug(f"Ответ: {new_data}")

            await websocket.send_text(new_data)

    except WebSocketDisconnect:
        logging.critical("Симулятор отключился")
