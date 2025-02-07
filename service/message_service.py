import json
from sockets import SIM_TYPE


def create_message_to_cli(data: str):
    if SIM_TYPE == "firefighter":
        client_id = json.loads(data)["id"]
        return client_id, data
    elif SIM_TYPE == "neuromorph":
        split_data = data.split(",")
        client_id = int(split_data[0])
        return client_id, ",".join(split_data[1:])


def create_message_to_sim(client_id: int, data: str):
    if SIM_TYPE == "firefighter":
        return data
    elif SIM_TYPE == "neuromorph":
        return f"{client_id},{data}"
