import asyncio
import json
from base64 import b64encode

import aiohttp

from constants import (
    EXPECTED_POST_STATUS,
    OUTBOUND_REQUEST_USER_NAME,
    OUTBOUND_REQUEST_PASSWORD
)
from exceptions import FailedPOSTRequest


def repeat(*, seconds: int):
    def _wraps(f):
        async def _wraps_f(*args, **kwargs):
            while True:
                await asyncio.sleep(seconds)
                await f(*args, **kwargs)
        return _wraps_f
    return _wraps


def _get_headers():
    user_and_pass_hash = b64encode(
        f'{OUTBOUND_REQUEST_USER_NAME}:{OUTBOUND_REQUEST_PASSWORD}'.encode('utf-8')
    )
    return {
        'Authorization': f'Basic {user_and_pass_hash}'
    }


async def post_request(url, body):
    headers = _get_headers()
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url, data=json.dumps(body)) as resp:
            if resp.status != EXPECTED_POST_STATUS:
                raise FailedPOSTRequest(
                    f'Received bad status attempting to {url} '
                    f'({resp.status} != {EXPECTED_POST_STATUS}'
                )
