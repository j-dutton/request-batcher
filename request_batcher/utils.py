import asyncio


def repeat(*, seconds: int):
    def _wraps(f):
        async def _wraps_f(*args, **kwargs):
            while True:
                await asyncio.sleep(seconds)
                await f(*args, **kwargs)
        return _wraps_f
    return _wraps
