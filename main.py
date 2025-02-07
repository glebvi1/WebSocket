import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/debug.log"
)


def create_message_to_cli(data: str):
    # split_data = data.split(",")
    # client_id = int(split_data[0])
    #
    # return client_id, ",".join(split_data[1:])
    import json
    client_id = json.loads(data)["id"]
    return client_id, data


def create_message_to_sim(client_id: int, data: str):
    return f"{client_id},{data}"


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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=41235, log_level="critical")
