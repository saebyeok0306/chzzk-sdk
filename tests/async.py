import asyncio
import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s\t- %(message)s", datefmt="%Y-%m-%d %H:%M:%S")


async def exec():
    logging.info("exec!!")


async def background_task(loop):
    logging.info("Background task running...")
    await asyncio.sleep(1)

    loop.create_task(exec())
    logging.info("Background task closed...")


async def timed_task(loop):
    try:
        logging.info("await wait_for(59)")
        await asyncio.wait_for(asyncio.sleep(60), timeout=59)
        logging.info("timed_task")
        await background_task(loop)
    except asyncio.TimeoutError:
        logging.info("Timeout in timed_task!")


async def main():
    loop = asyncio.get_event_loop()
    while True:
        await asyncio.create_task(timed_task(loop))  # await wait_for로 loop가 block됨.

if __name__ == "__main__":
    asyncio.run(main())