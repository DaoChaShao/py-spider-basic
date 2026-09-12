#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/12 22:02
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   decorator.py.py
# @Desc     :   

from functools import wraps
from time import perf_counter
from typing import Optional

WIDTH: int = 64


def beautifier(desc: Optional[str] = None):
    """
    Decorator to beautify function execution with start and completion logs.

    This decorator prints a visually separated log message before and after
    the decorated function runs. It helps track function execution flow in
    scripts or notebooks.

    :param desc: Optional custom name for the function shown in logs.
    :return: A wrapped function that adds logging around the original call.
    """

    def decorator(func):
        """
        Inner decorator that wraps the target function.

        :param func: The function to be decorated.
        :return: The wrapped function with beautification logic.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper that executes the function with beautified logs.

            :param args: Positional arguments passed to the original function.
            :param kwargs: Keyword arguments passed to the original function.
            :return: The return value of the original function.
            """
            _desc: str = desc or func.__name__

            print("*" * WIDTH)
            print(f"The function named {_desc!r} is starting:")
            print("-" * WIDTH)
            result = func(*args, **kwargs)
            print("-" * WIDTH)
            print(f"The function named {_desc!r} has completed.")
            print("*" * WIDTH)
            print()
            return result

        return wrapper

    return decorator


def timer(desc: Optional[str] = None):
    """
    Decorator to time function execution and log performance.

    This decorator measures the elapsed time of the decorated function
    and prints a formatted log with the execution duration.

    :param desc: Optional custom name for the function shown in logs.
    :return: A wrapped function that adds timing and logging around the original call.
    """

    def decorator(func):
        """
        Inner decorator that wraps the target function with timing logic.

        :param func: The function to be decorated.
        :return: The wrapped function with timing and beautification.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper that executes the function with timing and logs.

            :param args: Positional arguments passed to the original function.
            :param kwargs: Keyword arguments passed to the original function.
            :return: The return value of the original function.
            """
            _desc: str = desc or func.__name__

            print("*" * WIDTH)
            print(f"The function named {_desc!r} is starting:")
            print("-" * WIDTH)
            time_start = perf_counter()
            result = func(*args, **kwargs)
            time_end = perf_counter()
            time_elapsed = time_end - time_start
            print("-" * WIDTH)
            print(f"The function named {_desc!r} took {time_elapsed:.4f} seconds to complete.")
            print("*" * WIDTH)
            print()
            return result

        return wrapper

    return decorator


def clock(desc: Optional[str] = None):
    """
    Decorator to time function execution and log performance.

    This decorator measures the elapsed time of the decorated function
    and prints a formatted log with the execution duration.

    :param desc: Optional custom name for the function shown in logs.
    :return: A wrapped function that adds timing and logging around the original call.
    """

    def decorator(func):
        """
        Inner decorator that wraps the target function with timing logic.

        :param func: The function to be decorated.
        :return: The wrapped function with timing and beautification.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Wrapper that executes the function with timing and optional logs.

            :param args: Positional arguments passed to the original function.
            :param kwargs: Keyword arguments passed to the original function.
            :return: The return value of the original function.
            """
            _desc: str = desc or func.__name__
            _authorise: bool = kwargs.pop("display", True)

            if _authorise:
                print("*" * WIDTH)
                print(f"The function named {_desc!r} is starting:")
                print("-" * WIDTH)
                time_start = perf_counter()
                result = func(*args, **kwargs)
                time_end = perf_counter()
                time_elapsed = time_end - time_start
                print("-" * WIDTH)
                print(f"The function named {_desc!r} took {time_elapsed:.4f} seconds to complete.")
                print("*" * WIDTH)
                print()
            else:
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator
