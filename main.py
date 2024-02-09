from datetime import datetime
from funcs import *
from pprint import pprint
from models import init_db, People, Session

'''
На моем Windows 10 без блока "import platform" возвращается
"RuntimeError: Event loop is closed", даже если сам скрипт выполняется с "exit code 0"
'''
import platform
if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def main():
    async with ClientSession() as session:

        persons_quantity = await get_field_value(base_url, "count", session)
        persons_list = []
        persons_count = 0

        while persons_count < persons_quantity:
            if len(persons_list) == 0:
                first_id = 1
                last_id = persons_quantity + 1
            else:
                first_id = persons_list[-1]["id"] + 1
                last_id = first_id + persons_quantity - persons_count + 1
            for id_list in chunked(range(first_id, last_id), CHUNK_SIZE):
                persons_list = await create_persons_list(base_url, session, id_list)
                persons_count += len(persons_list)
                print(f"{len(persons_list) = }")
                pprint(persons_list)
                print()
                print()

    # asyncio.create_task(paste_to_db(*persons_list))

    # tasks_to_await = asyncio.all_tasks() - {asyncio.current_task()}
    # await asyncio.gather(*tasks_to_await)


if __name__ == '__main__':
    start_time = datetime.now()
    asyncio.run(main())
    print(datetime.now() - start_time)