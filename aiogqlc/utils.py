import io
from typing import Any


def is_file_like(variable: Any) -> bool:
    return isinstance(variable, io.IOBase)
