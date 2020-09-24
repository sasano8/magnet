from libs.decorators.impl import (
    Instantiate,
    Hook,
    Tag,
    PrintLog,
    Decode,
    MapDict,
    MapJson,
#     MapJsonAsync
)

from libs.decorators.abstract import (
    FuncDecorator
)

from libs.decorators.repository import (
    Repoisotry
)

class Decorator(FuncDecorator):
    def wrapper(self, func, *args, **kwargs):
        return
