from collections import UserDict


class AttrDict(UserDict):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.__dict__.update(self)
