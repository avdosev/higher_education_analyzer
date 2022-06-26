from aiohttp import ClientSession
_base_url = 'https://api.hh.ru'

async def get(session: ClientSession, url, params = None):
    async with session.get(url, params=params) as response:
        if response.status == 404:
            return None
        
        if response.status != 200:
            return None

        return await response.json()

async def find_by_keywords(session: ClientSession, key_words: str, page: int, page_size: int):
    _vacancies_url = 'vacancies'
    _true_string = 'true'
    _search_query_param = 'text'
    _premium_query_param = 'premium'
    _page_query_param = 'page'
    _page_size_query_param = 'per_page'
    
    url = f'{_base_url}/{_vacancies_url}'
    params = {
        _search_query_param: key_words,
        _premium_query_param: _true_string,
        _page_query_param: page,
        _page_size_query_param: page_size
    }

    async with session.get(url=url, params=params) as response:
        if response.status == 404:
            return []

        if response.status != 200:
            print(f'Cannot find vacancies by key words: {key_words}, page: {page}, page_size: {page_size}')
            print(response.status, await response.text())
            return []

        vacancy_list = await response.json()

    return vacancy_list

async def get_vacany(session: ClientSession, vacancy_id):
    response = await get(session, f'{_base_url}/vacancies/{vacancy_id}')

    if response is None:
        print(f'Cannot get vacancy with id: {vacancy_id}')
        return None

    return response