from asyncio import sleep as asleep

async def retryer(get, retry_times=1, retry_delay=0):
    for _ in range(retry_times):
        try:
            return await get()
        except Exception as exceptions:
            pass
        
        await asleep(retry_delay)

    raise exceptions
