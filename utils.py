def readlines(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read().splitlines()