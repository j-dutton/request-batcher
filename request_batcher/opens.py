import asyncio
import datetime
from functools import lru_cache

from aiohttp import web

from constants import (
    STATIC_FILE_LOC,
    OPEN_FLUSH_INTERVAL_SECONDS,
    TRACKING_ID_QUERY_PARAM,
    MAX_BATCH_TO_FLUSH,
    OPEN_DATA_POST_URL
)
from logger import LOG
from exceptions import RequestError
from state import OpenState, OpenData
from utils import repeat, post_request

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
    """View hit when email is opened.

    This will add a task (to log the open), and continue to respond without waiting without
    waiting for the task.
    """
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


@repeat(seconds=OPEN_FLUSH_INTERVAL_SECONDS)
async def flush_opens():
    """
    Code called when flushing the opens currently stored in state.

    This will fetch data from the OpenState (without mutating it), format, attempt to POST
    to the URL, and remove it on success.
    """
    to_flush, number_being_flushed = open_state.get_records_to_pop(number_of_records=MAX_BATCH_TO_FLUSH)

    # Format data
    formatted_to_flush = [
        {
            'tracking_id': open_data.tracking_id,
            'timestamp': open_data.timestamp.isoformat()
        } for open_data in to_flush
    ]

    # Attempt to make request
    try:
        await post_request(
            url=OPEN_DATA_POST_URL,
            body=formatted_to_flush
        )
    except RequestError:
        # TODO we could implement a retry policy here.
        LOG.getChild('flush_opens').exception('Failed to POST Opens')
        return

    # Remove the records from state on successful request
    open_state.pop_records(number_to_pop=number_being_flushed)
