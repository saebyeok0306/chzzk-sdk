import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s\t- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


async def background_task():
    logging.info("Background task running...")
    await asyncio.sleep(1)
    logging.info("Background task closed...")


async def timed_task():
    try:
        logging.info("await wait_for(59)")
        await asyncio.wait_for(asyncio.sleep(60), timeout=59)
        logging.info("timed_task")
    except asyncio.TimeoutError:
        logging.info("Timeout in timed_task!")


async def main():
    while True:
        await timed_task()  # await wait_for로 loop가 block됨.
        asyncio.create_task(background_task())  # wait_for 하는 동안, 작업을 비동기로 돌리고 싶음.

asyncio.run(main())