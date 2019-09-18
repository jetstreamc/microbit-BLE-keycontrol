import asyncio
from bleak import discover

async def run():
    devices = await discover()
    for d in devices:
        if 'BBC micro:bit' in d.name:
            print(d)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
