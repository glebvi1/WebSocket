import logging
import uvicorn

from sockets.server import app

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/debug.log"
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=41235, log_level="critical")
