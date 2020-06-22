import io
from typing import Any


def is_file_like(variable: Any) -> bool:
    return isinstance(variable, io.IOBase)


def is_file_list_like(variable: Any) -> bool:
    # True if variable is a non-empty list of io.IOBase instances
    return (
        isinstance(variable, list)
        and variable
        and all(isinstance(item, io.IOBase) for item in variable)
    )


def is_file_variable(variable: Any) -> bool:
    return is_file_like(variable) or is_file_list_like(variable)


def contains_file_variable(variables: dict) -> bool:
    for value in variables.values():
        if is_file_variable(value):
            return True
    return False


def filter_file_items(variables: dict) -> dict:
    return {
        key: value for key, value in variables.items() if not is_file_variable(value)
    }


def null_file_variables(variables: dict) -> dict:
    nulled_variables = dict()
    for key, value in variables.items():
        if is_file_like(value):
            nulled_variables[key] = None
        elif is_file_list_like(value):
            nulled_variables[key] = [None] * len(value)
        else:
            nulled_variables[key] = value
    return nulled_variables
