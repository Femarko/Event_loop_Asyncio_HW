from datetime import datetime
from funcs import *
from pprint import pprint

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
        last_id = persons_quantity + 1
        persons_list = []
        persons_list = await create_persons_list(last_id, base_url, session, persons_list=persons_list)
        if len(persons_list) < persons_quantity:
            first_id = persons_list[-1]["id"] + 1
            last_id = first_id + CHUNK_SIZE
            while len(persons_list) < persons_quantity:
                persons_list = await create_persons_list(last_id, base_url, session, first_id, persons_list)
        return persons_list


if __name__ == '__main__':
    start_time = datetime.now()
    pprint(asyncio.run(main()))
    print(datetime.now() - start_time)