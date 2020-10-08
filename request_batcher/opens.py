import asyncio
import datetime
from functools import lru_cache

from aiohttp import web

from constants import STATIC_FILE_LOC, TRACKING_ID_QUERY_PARAM
from state import OpenState, OpenData
from utils import repeat

open_state = OpenState()


async def handle_open(tracking_id: int, timestamp: datetime.datetime):
    open_state.add(
        OpenData(
            tracking_id=tracking_id,
            timestamp=timestamp
        )
    )


@lru_cache()
def _get_open_response():
    """Hold the file in memory for faster loading and less open file descriptors."""
    with open(STATIC_FILE_LOC, 'rb') as f:
        return f.read()


async def email_open(request):
    """View hit when email is opened."""
    params = request.rel_url.query
    tracking_id = params.get(TRACKING_ID_QUERY_PARAM)
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


@repeat(seconds=10)
async def flush_opens():
    records = await open_state.pop_records()
    print(f'Flushing {len(records)} records')
