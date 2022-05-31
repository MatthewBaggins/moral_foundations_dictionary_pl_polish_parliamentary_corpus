from functools import reduce
from operator import add
from typing import TypeVar

reduce_list = lambda ll: reduce(add, ll)

K = TypeVar('K'); V = TypeVar('V')
def dict_list_get(dl: list[dict[K, V]], k: K) -> list[V]:
    return [d[k] for d in dl if k in d]

Ko = TypeVar('Ko'); Ki = TypeVar('Ki')
def dict_dict_get(dd: dict[Ko, dict[Ki, V]], ki: Ki) -> dict[Ko, V]:
    return {ko: di[ki] for ko, di in dd.items() if ki in di}