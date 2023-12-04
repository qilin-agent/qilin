from pydantic import TypeAdapter
from typing import TypeVar
import dataclasses
import json


def json_dumps(data) -> str:
    return json.dumps(dataclasses.asdict(data))


T = TypeVar('T')
def json_loads(type: type[T], json_str: str) -> T:
    return TypeAdapter(type).validate_json(json_str)
