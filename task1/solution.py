import inspect
from functools import wraps


def strict(func):
    """
    Декоратор проверяет соответствие типов переданных в вызов функции аргументов
    типам аргументов, объявленным в прототипе функции.
    При несоответствии типов бросает исключение TypeError
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        signature = inspect.signature(func)
        bound_args = signature.bind(*args, **kwargs)
        bound_args.apply_defaults()

        annotations = func.__annotations__

        for name, value in bound_args.arguments.items():
            if name in annotations:
                expected_type = annotations[name]
                if not isinstance(value, expected_type):
                    raise TypeError(
                        f'Argument "{name}" must be of type {expected_type.__name__}, but got {type(value).__name__}')
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b
