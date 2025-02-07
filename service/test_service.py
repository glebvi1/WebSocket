import json
from tests import PATH_TEST


def save_dict_to_json(times):
    with open(PATH_TEST + "time.json", "w") as fp:
        json.dump(times, fp)
