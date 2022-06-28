# -*- coding: utf-8 -*-
import json
import os

def files_in_dir(dir):
    for (dirpath, dirnames, filenames) in os.walk(dir):
        for filename in filenames:
            yield os.path.join(dirpath, filename)

_keys = ['address', 'type', 'salary', 'schedule', 'employment', 'employer']
def remove_useless_keys(dict):
    for key in _keys:
        try:
            del dict[key]
        except KeyError:
            pass

data = []
data_id = []
ids = set()
for filename in files_in_dir(u'data/cache'):
    with open(filename) as d:
        for line in d:
            vacancy = json.loads(line)
            if vacancy['id'] in ids:
                continue
            remove_useless_keys(vacancy)
            ids.add(vacancy['id'])
            data_id.append(vacancy['id'])
            data.append(vacancy)




with open('data/vacancies.json', 'w') as f:
    json.dump(data, f, indent=2)

print('уникальных вакансий', len(ids))