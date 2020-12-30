import os
from pathlib import Path


def get_project_root() -> str:
    return str(Path(__file__).parent.parent.parent)


def bye(code=0):
    # noinspection PyProtectedMember
    os._exit(code)
