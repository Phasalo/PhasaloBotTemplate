import inspect


def filter_kwargs(func, kwargs: dict) -> dict:
    sig = inspect.signature(func)
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
    return kwargs if has_var_keyword else {k: v for k, v in kwargs.items() if k in sig.parameters}
