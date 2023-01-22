
class Utils:
    TileElementDirectionMask = 0b00000011
    RideTileType = 8

    def get_direction_with_offset(offset):
        return ((Utils.RideTileType & Utils.TileElementDirectionMask) + offset) & Utils.TileElementDirectionMask
    
    def floor2(x, y):
        return x & ~(y - 1)