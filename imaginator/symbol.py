"""
en = [A-Z]
ru = [А-Я]
sp = ' ' '?' '!' '=' '-' '+' '(' ')' '[' ']' '*' '.' ',' ';' ':' '/' '\' '<' '>' ''' '"' '#' '@' '%'
dg = [0-9]
"""


import os
from typing import Iterator, List, Tuple

from imaginator.imaginator import load_json_config


letters = load_json_config(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'letters.json'))


def get_symbol_mask(char: str, offset: int) -> List[Tuple[int, int]]:
    result = []
    mask = letters.get(char)

    if len(char) > 1 or mask is None:
        return result

    for row in range(len(mask)):
        for cell in range(len(mask[row])):
            if mask[row][cell]:
                result.append((row + offset, cell))

    return result


def get_str_mask(string: str, offset: int = 0) -> List[Tuple[int, int]]:
    result = []

    for symbol in string:
        result.extend(get_symbol_mask(symbol, offset))
        offset += len(letters[symbol]) + 1

    return result


def symbols_line_generator(string: str, reverse: bool = False) -> Iterator[List[int]]:
    for symbol in string:
        line = letters.get(symbol) or letters['?']
        yield from reversed(line) if reverse else line
        yield [0, 0, 0, 0, 0, 0, 0, 0, 0]
