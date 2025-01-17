import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="info.log"
)


def create_message(data: str):
    split_data = data.split(",")
    client_id = int(split_data[0])

    return ",".join(split_data[1:]), client_id


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
                await manager.send_to_sim(f"{client_id},{data}")

        elif answer == "its_sim":
            manager.connect_sim(websocket)

            while True:
                data = await websocket.receive_text()
                message, client_id = create_message(data)
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
