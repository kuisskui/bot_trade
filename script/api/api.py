import json
import sys
import typing


def get_state():
    return json.loads(sys.argv[1])


def update_state(current_state: typing.Dict, new_state: typing.Dict):
    return current_state | new_state


def end(state: typing.Dict):
    print(state)
