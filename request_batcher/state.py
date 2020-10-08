import asyncio
import datetime
from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class OpenData:
    tracking_id: int
    timestamp: datetime.datetime


class OpenState:
    """Note, there's nothing guaranteeing the order of _data, but it's correct enough."""

    def __init__(self):
        self._data: List[OpenData] = []
        self._lock = asyncio.Lock()

    def add(self, data: OpenData) -> None:
        self._data.append(data)

    async def pop_records(self, number_of_records: Optional[int]=None):
        async with self._lock:
            if number_of_records is not None:
                to_pop = self._data[:number_of_records]
                self._data = self._data[number_of_records:]
            else:
                to_pop = self._data
                self._data = []

            return to_pop

    def __len__(self):
        return len(self._data)
