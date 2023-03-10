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


class ImageIdOffset:
    def __init__(self):
        self.id = ""
        self.entries = []
    
    def add_entry(self, key, values):
        key_dict = key.to_dict()
        key_dict["imageIdOffset"] = values
        self.entries.append(key_dict)
    
    def to_dict(self):
        return { "id": self.id, "entries": self.entries }

class BoundBoxEntry:
    def __init__(self):
        self.id = ""
        self.values = []
    def add_value(self, value):
        self.values.append(value.to_dict())
    def to_dict(self):
        return {"id": self.id, "values": self.values}

class BoundBoxEntryValue:
    def __init__(self):
        self.coords = Coords(0, 0, 0)
        self.bound_box = BoundBox(Coords(0, 0, 0), Coords(0, 0, 0))
        self.key = PaintStructKey()
    def to_dict(self):
        result = self.key.to_dict()
        result["offset_x"] = self.coords.x
        result["offset_y"] = self.coords.y
        result["offset_z"] = self.coords.z

        result["bb_offset_x"] = self.bound_box.offset.x
        result["bb_offset_y"] = self.bound_box.offset.y
        result["bb_offset_z"] = self.bound_box.offset.z

        result["bb_length_x"] = self.bound_box.length.x
        result["bb_length_y"] = self.bound_box.length.y
        result["bb_length_z"] = self.bound_box.length.z
        return result
    

class PaintStructKey:
    def __init__(self):
        self.element = None
        self.direction = None
        self.track_sequence = None
        self.vehicle_index = None
        self.vehicle_sprite_direction = None
        self.vehicle_pitch = None
        self.vehicle_num_peeps = None
        self.vehicle_restraints_position = None
        self.session_current_rotation = None
    
    def to_dict(self):
        result = {}

        if self.element != None:
            result["trackElement"] = self.element

        if self.track_sequence != None:
            result["trackSequence"] = self.track_sequence
        
        if self.vehicle_index != None:
            result["vehicleIndex"] = self.vehicle_index
        
        if self.vehicle_sprite_direction != None:
            result["vehicleSpriteDirection"] = self.vehicle_sprite_direction

        if self.vehicle_pitch != None:
            result["vehiclePitch"] = self.vehicle_pitch
        
        if self.vehicle_num_peeps != None:
            result["vehicleNumPeeps"] = self.vehicle_num_peeps
        
        if self.direction != None:
            result["direction"] = self.direction
        
        if self.session_current_rotation != None:
            result["sessionCurrentRotation"] = self.session_current_rotation
        
        if self.vehicle_restraints_position != None:
            result["vehicleRestraintsPosition"] = self.vehicle_restraints_position
        
        return result

        

class PaintStruct:
    def __init__(self):
        #keys
        self.key = PaintStructKey()

        #outputs
        self.supports = None
        self.supports_type = None
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
        self.image_id_offset_index = None
        self.boundbox_id = None
        self.height_supports = None

    def to_dict(self):
        result = self.key.to_dict()
        
        if self.supports != None:
            result["supports"] = self.supports
        
        if self.supports_type != None:
            result["supportsType"] = self.supports_type

        if self.floor != None:
            result["floor"] = self.floor
        
        if self.edges != None:
            result["edges"] = self.edges
        
        if self.fences != None:
            result["fences"] = self.fences
        
        if self.paint_type != None:
            result["paintType"] = self.paint_type
        
        if self.image_id_base != None:
            result["imageIdBase"] = self.image_id_base

        if self.primary_colour != None:
            result["primaryColour"] = self.primary_colour
        
        if self.secondary_colour != None:
            result["secondaryColour"] = self.secondary_colour
        
        if self.primary_colour_index != None:
            result["primaryColourIndex"] = self.primary_colour_index
        
        if self.secondary_colour_index != None:
            result["secondaryColourIndex"] = self.secondary_colour_index
        
        if self.image_id_offset != None:
            result["imageIdOffset"] = self.image_id_offset
        
        if self.image_id_offset_index != None:
            result["imageIdOffsetIndex"] = self.image_id_offset_index
        
        if self.image_id_scheme != None:
            result["imageIdScheme"] = self.image_id_scheme
        
        if self.boundbox_id != None:
            result["boundBoxId"] = self.boundbox_id
        
        if self.height_supports != None:
            result["supportsHeightId"] = self.height_supports
        
        return result

class PaintStructKeyRange:
    def __init__(self):
        self.Elements = []
        self.Directions = []
        self.TrackSequences = []
        self.VehicleNumPeeps = []
        self.VehiclePitches = []
        self.VehicleRestraintsPositions = []
        self.VehicleSpriteDirections = []
        self.SessionCurrentRotations = []
    
    def to_dict(self):
        result = {}

        if len(self.Elements) > 0:
            result["elements"] = self.Elements
        
        if len(self.Directions) > 0:
            result["directions"] = self.Directions
        
        if len(self.TrackSequences) > 0:
            result["trackSequences"] = self.TrackSequences
        
        if len(self.VehicleNumPeeps) > 0:
            result["vehicleNumPeeps"] = self.VehicleNumPeeps
        
        if len(self.VehiclePitches) > 0:
            result["vehiclePitches"] = self.VehiclePitches
        
        if len(self.VehicleSpriteDirections) > 0:
            result["vehicleSpriteDirections"] = self.VehicleSpriteDirections
        
        if len(self.SessionCurrentRotations) > 0:
            result["sessionCurrentRotations"] = self.SessionCurrentRotations
        
        if len(self.VehicleRestraintsPositions) > 0:
            result["vehicleRestraintsPositions"] = self.VehicleRestraintsPositions
        return result