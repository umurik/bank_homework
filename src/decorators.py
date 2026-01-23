from contextlib import nullcontext, redirect_stdout
from functools import wraps
from io import StringIO
from time import time
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(filename: str = "") -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for logging function execution.

    Logs information about function start, result, execution time, and errors.
    Output can be written to a file or displayed in the console.

    Args:
        filename: Path to the log file. If empty string (default), logs are
                  printed to console. If specified, logs are written to file.

    Returns:
        Decorated function with added logging functionality.
    """

    def wrapper(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def inner(*args: P.args, **kwargs: P.kwargs) -> R:
            output_buffer = StringIO()
            context = redirect_stdout(output_buffer) if filename != "" else nullcontext()
            try:
                with context:
                    print(f"Starting function {func.__name__}")
                    time_start = time()
                    result = func(*args, **kwargs)
                    time_end = time()
                    print(f"Function result: {result}")
                    print("Finishing...")
                    print(f"Elapsed time {(time_end - time_start):.3f}")
                    return result
            except Exception as e:
                with context:
                    print(f"Errors occurred, when execution: {e}")
                    print(f"Args: {[x for x in args]}, kwargs: {[x for x in kwargs]}")
                raise e
            finally:
                if filename != "":
                    with open(filename, "w") as f:
                        f.write(output_buffer.getvalue())

        return inner

    return wrapper
