from clicks import click_state
from constants import MONITOR_INTERVAL_SECONDS, MAX_OPENS_ALLOWED_IN_STATE, MAX_CLICKS_ALLOWED_IN_STATE
from logger import LOG
from opens import open_state
from utils import repeat


@repeat(seconds=MONITOR_INTERVAL_SECONDS)
async def monitor():
    logger = LOG.getChild('monitor')
    logger.info('Running Monitor')
    awaiting_open_batch = len(open_state)
    awaiting_click_batch = len(click_state)

    # Opens
    if awaiting_open_batch > 0:
        logger.info('Batch of OpenData currently awaiting processing', extra={'length': awaiting_open_batch})

    if awaiting_open_batch > MAX_OPENS_ALLOWED_IN_STATE:
        logger.error(
            'Too many OpenData stuck in memory. Dropping all of them.',
            extra={'length': awaiting_open_batch}
        )
        await open_state.flush_all()

    # Clicks
    if awaiting_click_batch > 0:
        logger.info('Batch of ClickData currently awaiting processing', extra={'length': awaiting_click_batch})

    if awaiting_click_batch > MAX_CLICKS_ALLOWED_IN_STATE:
        logger.error(
            'Too many ClickData stuck in memory. Dropping all of them.',
            extra={'length': awaiting_click_batch}
        )
        await click_state.flush_all()
