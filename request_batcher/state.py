import asyncio
import datetime
from dataclasses import dataclass
from typing import Optional, Tuple, List, Iterable

from exceptions import BadArgumentError


@dataclass(frozen=True)
class DataToLog:
    tracking_id: int
    timestamp: datetime.datetime


class State:
    """Note, there's nothing guaranteeing the order of _data, but it's correct enough."""

    def __init__(self):
        self._data: List[DataToLog] = []
        self._lock = asyncio.Lock()

    def add(self, data: DataToLog) -> None:
        self._data.append(data)

    def get_records_to_pop(self, number_of_records: Optional[int]=None) -> Tuple[Iterable[DataToLog], int]:
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

        # Make sure we lock the object so that we don't attempt to pop twice at once and
        # leave ourselves in a bad state
        async with self._lock:
            self._data = self._data[number_to_pop:]

    async def flush_all(self):
        async with self._lock:
            self._data = []

    def __len__(self):
        return len(self._data)
