import datetime
from collections import UserDict
from typing import Optional


class AttrDict(UserDict):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.__dict__.update(self)
