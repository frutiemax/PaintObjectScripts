from .TrackElement import TrackElement
from .BoundBox import BoundBox
from .Coords import Coords

TrackMap3x3 = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8],
    [0, 3, 5, 7, 2, 8, 1, 6, 4],
    [0, 7, 8, 6, 5, 4, 3, 1, 2],
    [0, 6, 4, 1, 8, 2, 7, 3, 5]
]
class ImageIdBase:
    Car0 = "car0"

class Colour:
    VehicleBody = "vehicleBody"
    VehicleTrim = "vehicleTrim"
    PeepTShirt = "peepTShirt"

class SupportsType:
    WoodenA = "wooden_a"

class Scheme:
    Misc = "misc"
    Track = "track"

class FloorType:
    Cork = "cork"

class FenceType:
    Ropes = "ropes"

class PaintType:
    AddImageAsParent = "addImageAsParent"
    AddImageAsChild = "addImageAsChild"
    SetSegmentsSupportsHeight = "setSegmentSupportHeight"

class Edge:
    NE = "ne"
    SE = "se"
    SW = "sw"
    NW = "nw"

class Segment:
    B4 = "b4"
    CC = "cc"
    BC = "bc"
    D4 = "d4"
    C0 = "c0"
    D0 = "d0"
    B8 = "b8"
    C8 = "c8"
    C4 = "c4"


class PaintStruct:
    def __init__(self):
        #keys
        self.element = TrackElement.FlatTrack3x3
        self.direction = None
        self.track_sequence = None
        self.track_sequence_mapping = None
        self.vehicle_index = None
        self.vehicle_sprite_direction = None
        self.vehicle_pitch = None
        self.vehilce_num_peeps = None

        #outputs
        self.supports = None
        self.floor = None
        self.edges = None
        self.fences = None
        self.paint_type = None
        self.image_id_scheme = None
        self.image_id_base = None
        self.primary_colour = None
        self.primary_colour_index = None
        self.secondary_colour = None
        self.secondary_colour_index = None
        self.image_id_offset = None
        self.offset = None
        self.boundbox = None
        self.height_supports = None

    def to_dict(self):
        result = {}
        result["trackElement"] = self.element

        if self.track_sequence_mapping != None:
            result["trackSequenceMapping"] = self.track_sequence_mapping
        
        if self.supports != None:
            result["supports"] = self.supports

        if self.floor != None:
            result["floor"] = self.floor
        
        if self.edges != None:
            result["edges"] = self.edges
        
        if self.fences != None:
            result["fences"] = self.fences
        
        if self.track_sequence != None:
            result["trackSequence"] = self.track_sequence
        
        if self.direction != None:
            result["direction"] = self.direction
        
        if self.paint_type != None:
            result["paintType"] = self.paint_type
        
        if self.image_id_base != None:
            result["imageIdBase"] = self.image_id_base
        
        if self.image_id_offset != None:
            result["imageIdOffset"] = self.image_id_offset
        
        if self.image_id_scheme != None:
            result["imageIdScheme"] = self.image_id_scheme
        
        if self.offset != None:
            result["offset_x"] = self.offset.x
            result["offset_y"] = self.offset.y
            result["offset_z"] = self.offset.z
        
        if self.boundbox != None:
            result["bb_offset_x"] = self.boundbox.offset.x
            result["bb_offset_y"] = self.boundbox.offset.y
            result["bb_offset_z"] = self.boundbox.offset.z
            result["bb_length_x"] = self.boundbox.length.x
            result["bb_length_y"] = self.boundbox.length.y
            result["bb_length_z"] = self.boundbox.length.z
        
        if self.height_supports != None:
            result["supportsHeightId"] = self.height_supports
        
        return result