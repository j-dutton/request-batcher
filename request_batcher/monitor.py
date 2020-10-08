from opens import open_state
from utils import repeat


@repeat(seconds=1)
async def monitor():
    print(f'Batch of {len(open_state)} awaiting processing')
