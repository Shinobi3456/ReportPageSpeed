from itertools import product
import string


def generate():
    i = 0
    while True:
        i += 1
        for x in product(string.ascii_lowercase, repeat=i):
            yield ''.join(x)


def generateRangeSheets(generator):
    start = next(generator).upper()
    next(generator).upper()
    end = next(generator).upper()
    
    return [start, end]