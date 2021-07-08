from typing import Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Feed:
    name: str
    url: str
    icon: Optional[str]
    last_published_datetime: datetime
