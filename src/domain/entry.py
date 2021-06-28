from typing import List
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Keyword:
    word: str
    score: float


@dataclass(frozen=True)
class Entry:
    title: str
    url: str
    summary: str
    image: str
    language: str
    text: str
    published_date: datetime
    keywords: List[Keyword]
