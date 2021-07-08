try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from typing import List
from dataclasses import dataclass


ShortType = Literal["true", "false"]


@dataclass(frozen=True)
class SlackField:
    title: str
    value: str
    short: ShortType


@dataclass(frozen=True)
class SlackAttachment:
    author_name: str
    author_link: str
    author_icon: str
    fallback: str
    color: str
    title: str
    title_link: str
    image_url: str
    text: str
    footer: str
    footer_icon: str
    ts: int
    fields: List[SlackField]


@dataclass(frozen=True)
class SlackOutputData:
    username: str
    attachments: List[SlackAttachment]
