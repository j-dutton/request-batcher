from constants import MONITOR_INTERVAL_SECONDS, MAX_OPENS_ALLOWED_IN_STATE
from logger import LOG
from opens import open_state
from utils import repeat


@repeat(seconds=MONITOR_INTERVAL_SECONDS)
async def monitor():
    logger = LOG.getChild('monitor')
    logger.info('Running Monitor')
    awaiting_batch = len(open_state)

    if awaiting_batch > 0:
        logger.info('Batch of OpenData currently awaiting processing', extra={'length': awaiting_batch})

    if awaiting_batch > MAX_OPENS_ALLOWED_IN_STATE:
        logger.error(f'Too many OpenData stuck in memory. Dropping all of them.', extra={'length': awaiting_batch})
        _, number_to_drop = open_state.get_records_to_pop(number_of_records=awaiting_batch)
        await open_state.pop_records(number_to_pop=number_to_drop)
