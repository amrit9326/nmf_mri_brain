from typing import Any, Sequence, Callable, Type, Iterable
import inspect
from itertools import accumulate
from functools import partial
from operator import mul
from torch import nn
PositionalArgs = tuple[Any, ...]
KeywordArgs = dict[str, Any]
ArgsType = PositionalArgs | KeywordArgs
PartialFunctionType = tuple[Callable[..., Any] | ArgsType, ...]
PartialModuleType = tuple[Type[nn.Module] | ArgsType, ...]

class Universaltuple(tuple):

    def __contains__(self, other: Any) -> bool:
        return True

def as_tuple(obj: Any) -> tuple[Any, ...]:
    if not isinstance(obj, Sequence) or isinstance(obj, str):
        return (obj,)
    return tuple(obj)

def cumprod(x: Iterable[float]) -> list[float]:
    return list(accumulate(x, mul))

def has_args(obj: Any, keywords: str | Sequence[str]) -> bool:
    if not callable(obj):
        return False
    try:
        sig = inspect.signature(obj)
    except ValueError:
        return False
    return all((key in sig.parameters for key in as_tuple(keywords)))

def partialize(obj: PartialFunctionType) -> Callable:
    if callable(obj):
        return obj
    if isinstance(obj, Sequence) and callable(obj[0]):
        callable_obj = obj[0]
        args = []
        kwargs = {}
        for item in obj[1:]:
            if isinstance(item, dict):
                kwargs.update(item)
            elif isinstance(item, Sequence) and (not isinstance(item, str)):
                args.extend(item)
            else:
                args.append(item)
        return partial(callable_obj, *args, **kwargs)
    raise TypeError(f'Expected a callable or valid tuple, got {type(obj).__name__}')

def is_partializable(obj: Any) -> bool:
    if callable(obj):
        return True
    if isinstance(obj, Sequence) and obj and callable(obj[0]):
        return True
    return False