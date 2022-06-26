from ast import keyword
import asyncio
from aiohttp import ClientSession
from api import *
import json
import os

base_dir = 'data'
output_dir = 'data/vacancies_by_keyword'

async def main():
    # prepare
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(base_dir, exist_ok=True)
    start_from = None
    # run
    
    async with ClientSession() as session:
        keywords = readlines('keywords.txt')
        
        for keyword in keywords:
            with open(f'{output_dir}/{"_".join(keyword.split(" "))}.json', 'a') as bf:
                find_result = await find_by_keywords(session, keyword, 0, 50)
                if find_result is None:
                    continue
                ids = extract_ids(find_result)
                vacancies = await asyncio.gather(*[asyncio.create_task(get_vacany(session, id)) for id in ids])
                bump_list(bf, vacancies)
                with open(f'{base_dir}/log.json', 'w', encoding='utf-8') as f:
                    json.dump(vacancies, f, indent=2, ensure_ascii=False)

def extract_ids(vacancies):
    for vacancy in vacancies['items']:
        yield vacancy['id']

def bump_list(f, data_list):
    for data in data_list:
        if data is None:
            continue
        print(json.dumps(data), file=f)

def readlines(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read().splitlines()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())