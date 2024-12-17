"""Module for indented printing; both automatically and manually.

.. code-block:: python

    from plox.print import indent_print
"""

import inspect
from itertools import count
from sys import _getframe
from typing import Optional


def stack_size(size: int = 0) -> int:
    """Get stack size for caller's frame."""
    frame = _getframe(size)
    for size in count(size):  # noqa: B020
        frame = frame.f_back
        if not frame:
            return size

    return size


def indent_print(msg: str, indent_level: Optional[int] = None, indent_char: str = "|- ") -> None:
    """Print a message with an appropriately indented prefix.

    Example:

        >>> from plox.print.indent_print import indent_print as printi
        >>>
        >>> def test():
        ...     printi("inside test")
        >>>
        >>> def test2():
        ...     printi("inside test2")
        ...     test()
        >>>
        >>> def test3():
        ...     printi("This it the inside of test3")
        ...     test2()
        ...     test()
        >>>
        >>> test3()
        |- test3():This it the inside of test3
        |- |- test2():inside test2
        |- |- |- test():inside test
        |- |- test():inside test


    Args:
        msg (str): Message to print.
        indent_level (Optional[int]): Level to print at; if not given, will be determined
            automatically by stack/frame depth.
        indent_char (str): Set of chars to prefix the indents with.
    """
    parent = inspect.stack()[1][3]

    if type(msg) is not str:
        msg = str(msg)

    if indent_level is not None:
        print(f"{indent_level*indent_char}{parent}():{msg}")  # noqa: T201
        return

    depth = stack_size() - 2
    print(f"{depth*indent_char}{parent}():{msg}")  # noqa: T201
