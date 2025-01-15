from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from ConnectionManager import ConnectionManager

app = FastAPI()
manager = ConnectionManager()


@app.websocket("/")
async def websocket_sim(websocket: WebSocket):
    await websocket.accept()
    try:
        await websocket.send_text("who_r_u")
        answer = await websocket.receive_text()

        if answer == "its_cli":
            client_id = await manager.connect_cli(websocket)

            while True:
                data = await websocket.receive_text()
                # print(f"Данные с клиента №{client_id}: ", data)
                await manager.send_to_sim(f"{client_id},{data}")

        elif answer == "its_sim":
            manager.sim = websocket
            print("Симулятор подключен:", websocket)

            while True:
                data = await websocket.receive_text()
                split_data = data.split(",")
                client_id = int(split_data[0])
                # print(f"Отправлено клиенту №{client_id}:", ",".join(split_data[1:]))
                await manager.send_to_cli(client_id, ",".join(split_data[1:]))
    except WebSocketDisconnect:
        await manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=41235, log_level="critical")
