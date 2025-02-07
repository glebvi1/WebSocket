import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from service.message_service import create_message_to_cli, create_message_to_sim
from sockets.ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/")
async def websocket_sim(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("who_r_u")
        answer = await websocket.receive_text()

        if answer == "its_cli":
            logging.debug("Подключение нового клиента...")
            client_id = await manager.connect_cli(websocket)

            while True:
                data = await websocket.receive_text()
                await manager.send_to_sim(client_id, create_message_to_sim(client_id, data))

        elif answer == "its_sim":
            manager.connect_sim(websocket)

            while True:
                data = await websocket.receive_text()
                client_id, message = create_message_to_cli(data)
                await manager.send_to_cli(client_id, message)

    except WebSocketDisconnect:
        if manager.sim == websocket:
            manager.sim = None
            logging.critical("Симулятор отключился")
        else:
            await manager.disconnect(websocket)
