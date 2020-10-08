import asyncio
import datetime
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

from aiohttp import web


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


opens = OpenState()


async def handle_open(tracking_id: int, timestamp: datetime.datetime):
    opens.add(
        OpenData(
            tracking_id=tracking_id,
            timestamp=timestamp
        )
    )


@lru_cache()
def _get_open_response():
    with open('static/pixel.png', 'rb') as f:
        return f.read()


async def email_open(request):
    params = request.rel_url.query
    tracking_id = params.get('tracking_id')
    if tracking_id is not None:
        asyncio.create_task(
            handle_open(
                tracking_id=tracking_id,
                timestamp=datetime.datetime.now()
            )
        )

    resp = web.StreamResponse(headers={'Content-Type': 'image/png'})
    await resp.prepare(request)
    await resp.write(_get_open_response())
    return resp


def repeat(*, seconds: int):
    def _wraps(f):
        async def _wraps_f(*args, **kwargs):
            while True:
                await asyncio.sleep(seconds)
                await f(*args, **kwargs)
        return _wraps_f
    return _wraps


@repeat(seconds=10)
async def flush_opens():
    records = await opens.pop_records()
    # print(f'Flushing {len(records)} records')


@repeat(seconds=1)
async def monitor():
    pass
    # print(f'Batch of {len(opens)} awaiting processing')


async def main():
    app = web.Application()
    app.add_routes([web.get('/open_tracking/', email_open)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)

    await asyncio.gather(
        site.start(),
        flush_opens(),
        monitor(),
    )


if __name__ == '__main__':
    asyncio.run(main())
