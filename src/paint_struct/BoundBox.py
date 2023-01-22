from .Coords import *

class BoundBox:
    def __init__(self, offset=Coords(), length=Coords()):
        self.offset = offset
        self.length = length