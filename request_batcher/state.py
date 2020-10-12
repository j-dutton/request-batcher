import asyncio
import datetime
from dataclasses import dataclass
from typing import Optional, Tuple, List, Iterable

from exceptions import BadArgumentError


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

    def get_records_to_pop(self, number_of_records: Optional[int]=None) -> Tuple[Iterable[OpenData], int]:
        if number_of_records is None:
            number_of_records = len(self._data)

        to_pop = self._data[:number_of_records]
        return to_pop, len(to_pop)

    async def pop_records(self, number_to_pop: int):
        current_records = len(self)
        if number_to_pop > current_records:
            raise BadArgumentError(
                f'Attempting to pop too many values from {self.__class__.__name__} '
                f'({number_to_pop} > {current_records})'
            )

        async with self._lock:
            self._data = self._data[number_to_pop:]

    def __len__(self):
        return len(self._data)
