from typing import Union
from dataclasses import dataclass
from datetime import datetime

U = Union[str, None]


@dataclass
class Feed:
    name: str
    url: str
    icon: U
    last_published_datetime: datetime
