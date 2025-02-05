H = 400
kp, ki, kd = 7, 0.8, 0.3
dt = 0.1

data_for_pid = {}


def check_client(client_id: int):
    if client_id not in data_for_pid:
        data_for_pid[client_id] = {
            "x": [0, 0],  # integral_x, prevision_error_x
            "y": [0, 0],  # integral_y, prevision_error_y
            "z": [0, 0],  # integral_z, prevision_error_z
        }


def constrain(x, min_value=-200, max_value=200):
    if x < min_value:
        return min_value
    if x > max_value:
        return max_value
    return x


def compute_PID(id: int, current_coord: float, dot: float, coord: str):
    error = dot - current_coord
    data_for_pid[id][coord][0] = constrain(data_for_pid[id][coord][0] + error * dt * ki)
    d = (error - data_for_pid[id][coord][1]) / dt
    data_for_pid[id][coord][1] = error

    return constrain(error * kp + data_for_pid[id][coord][0] + d * kd)


def analyze(data):
    "data: id, rotationX, rotationY, rotationZ, positionX, positionZ, positionY, dotX, dotY"
    client_id, rotation_x, rotation_y, rotation_z, position_x, position_z, position_y, dot_x, dot_y\
        = list(map(float, data.split(",")))

    check_client(client_id)

    x_speed = compute_PID(client_id, position_x, dot_x, "x")
    y_speed = compute_PID(client_id, position_y, dot_y, "y")
    speed = compute_PID(client_id, position_z, H, "z")

    speed_top_right = str(speed + y_speed)
    speed_top_left = str(speed + x_speed)
    speed_bottom_right = str(speed - y_speed)
    speed_bottom_left = str(speed - x_speed)

    return ",".join([speed_top_right, speed_top_left, speed_bottom_right, speed_bottom_left])
