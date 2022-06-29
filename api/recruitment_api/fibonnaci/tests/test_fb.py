from typing import Callable, Dict, List, Tuple
import pytest
from fibonnaci.fixtures import time_tracker
from fibonnaci.cached import fibonacci_cached, fibonacci_lru_cached
from fibonnaci.naive import fibonacci_naive


def get_list_of_kwargs_for_function(
    identifiers: str, values: List[Tuple[str, str]]
) -> List[Dict[str, str]]:
    print(f"getting list of kwargs for function, \n{identifiers=}, {values=}")
    parsed_identifiers = identifiers.split(",")
    list_of_kwargs_for_function = []
    for tuple_value in values:
        kwargs_for_function = {}
        for i, keyword in enumerate(parsed_identifiers):
            kwargs_for_function[keyword] = tuple_value[i]
        list_of_kwargs_for_function.append(kwargs_for_function)

    print(f"{list_of_kwargs_for_function=}")
    return list_of_kwargs_for_function


Decorator = Callable


def my_parametrized(identifiers: str, values: List[Tuple[int, int]]) -> Decorator:
    def my_parametrized_decorator(function: Callable) -> Callable:
        def run_func_parametrized() -> None:
            list_of_kwargs_for_function = get_list_of_kwargs_for_function(
                identifiers=identifiers, values=values
            )
            for kwargs_for_function in list_of_kwargs_for_function:
                print(
                    f"calling function {function.__name__} with {kwargs_for_function= }"
                )
                function(**kwargs_for_function)

        return run_func_parametrized

    return my_parametrized_decorator


# @pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
@my_parametrized(identifiers="n,expected", values=[(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_naive(n: int, expected: int) -> None:
    res = fibonacci_naive(n)
    assert res == expected

@my_parametrized(identifiers="n,expected", values=[(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_cached(n: int, expected: int) -> None:
    res = fibonacci_cached(n)
    assert res == expected


# Refactor
@pytest.mark.parametrize("fib_func", [fibonacci_naive, fibonacci_cached, fibonacci_lru_cached])
@pytest.mark.parametrize("n,expected", [(0, 0), (1, 1), (2, 1), (20, 6765)])
def test_fibonacci(time_tracker, fib_func: Callable[[int], int], n: int, expected: int) -> None:
    res = fib_func(n)
    assert res == expected
