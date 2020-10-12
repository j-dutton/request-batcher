import asyncio

from aiohttp import web

from clicks import email_click, flush_clicks
from opens import email_open, flush_opens
from monitor import monitor
from constants import OPEN_TRACKING_URL, CLICK_TRACKING_URL


async def main():
    # Setup the site
    app = web.Application()
    app.add_routes(
        [
            web.get(OPEN_TRACKING_URL, email_open),
            web.get(CLICK_TRACKING_URL, email_click),
        ]
    )
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner)

    # Add flushing + monitoring
    await asyncio.gather(
        site.start(),
        flush_opens(),
        flush_clicks(),
        monitor(),
    )


if __name__ == '__main__':
    asyncio.run(main())
