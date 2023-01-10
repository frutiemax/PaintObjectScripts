from paint_struct.PaintStruct import *
from paint_struct.PaintObjectFile import *
from paint_struct.HeightSupportsTable import *
from paint_struct.TrackElement import *
from paint_struct.Coords import *
from paint_struct.BoundBox import *
from paint_struct.TrackSequenceTable import *
from paint_struct.EdgeTable import *

def paint_circus_tent(circus_structure, direction, al, cl):
    circus_structure.offset = Coords(al, cl, 3)
    circus_structure.boundbox = BoundBox(Coords(al + 16, cl + 16, 3), Coords(24, 24, 47))
    circus_structure.paint_type = PaintType.AddImageAsParent
    circus_structure.image_id_base = ImageIdBase.Car0

def paint_circus(paint_object, track_element, direction, track_sequence,
    vehicle_index, vehicle_sprite_direction, vehicle_pitch, vehicle_num_peeps):

    circus_structure = PaintStruct()
    circus_structure.key.element = track_element
    circus_structure.key.direction = direction
    circus_structure.image_id_offset = "direction"
    
    #transform the track sequence with the track map
    track_sequence = TrackMap3x3[direction][track_sequence]
    circus_structure.key.track_sequence = track_sequence

    match track_sequence:
        case 1:
            paint_circus_tent(circus_structure, direction, 32, 32)
            paint_object.add_paint_struct(circus_structure)
        case 3:
            paint_circus_tent(circus_structure, direction, 32, -32)
            paint_object.add_paint_struct(circus_structure)
        case 5:
            paint_circus_tent(circus_structure, direction, 0, -32)
            paint_object.add_paint_struct(circus_structure)
        case 6:
            paint_circus_tent(circus_structure, direction, -32, 32)
            paint_object.add_paint_struct(circus_structure)
        case 7:
            paint_circus_tent(circus_structure, direction, -32, -32)
            paint_object.add_paint_struct(circus_structure)
        case 8:
            paint_circus_tent(circus_structure, direction, -32, 0)
            paint_object.add_paint_struct(circus_structure)

def generate_json():
    #generate all the possible combinations to pass through the function
    track_sequences = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    directions = [0, 1, 2, 3]
    track_element = TrackElement.FlatTrack3x3

    paint_object = PaintObjectFile()

    #floor + fences + supports
    base_paint_struct = PaintStruct()
    base_paint_struct.track_sequence_mapping = "track_map_3x3"
    base_paint_struct.edges = "edges_3x3"
    base_paint_struct.supports = SupportsType.WoodenA
    base_paint_struct.image_id_scheme = Scheme.Misc
    base_paint_struct.floor = FloorType.Cork
    base_paint_struct.fences = FenceType.Ropes
    base_paint_struct.element = track_element
    paint_object.add_paint_struct(base_paint_struct)
    
    for track_sequence in track_sequences:
        for direction in directions:
            paint_circus(paint_object, track_element, direction, track_sequence, None, None, None, None)
    
    #height supports
    height_supports = PaintStruct()
    height_supports.element = track_element
    height_supports.track_sequence_mapping = "track_map_3x3"
    height_supports.paint_type = PaintType.SetSegmentsSupportsHeight
    height_supports.height_supports = "heightSupports_3x3"
    paint_object.add_paint_struct(height_supports)

    sequenceTable = TrackSequenceTable()
    sequenceTable.trackElement = TrackElement.FlatTrack3x3
    sequenceTable.sequences = TrackMap3x3
    paint_object.add_sequence_table(sequenceTable)

    edgeTable = EdgeTable()
    edgeTable.id = "edges_3x3"
    edgeTable.edges = [
        [],
        [Edge.NE, Edge.NW],
        [Edge.NE],
        [Edge.NE, Edge.SE],
        [Edge.NW],
        [Edge.SE],
        [Edge.SW, Edge.NW],
        [Edge.SW, Edge.SE],
        [Edge.SW]]
    paint_object.add_edge_table(edgeTable)

    directionImageId = ImageIdOffset()
    directionImageId.id = "direction"
    values = [0, 1, 2, 3]
    for value in values:
        key = PaintStructKey()
        key.direction = value
        directionImageId.add_entry(key, [value])
    paint_object.add_image_id_offset(directionImageId)
    
    height_supports = HeightSupportsTable()
    height_supports.height_offset = 128
    height_supports.add_support_segment(HeightSupportsSegment(1, [Segment.B4, Segment.C8, Segment.CC]))
    height_supports.add_support_segment(HeightSupportsSegment(3, [Segment.CC, Segment.BC, Segment.D4]))
    height_supports.add_support_segment(HeightSupportsSegment(6, [Segment.C8, Segment.B8, Segment.D0]))
    height_supports.add_support_segment(HeightSupportsSegment(7, [Segment.D0, Segment.C0, Segment.D4]))
    height_supports.id = "heightSupports_3x3"
    paint_object.add_height_support_table(height_supports)

    paint_object.set_object_id("openrct2.paint.circus")
    paint_object.set_object_version("1.0")
    paint_object.add_author("OpenRCT2 Developpers")
    paint_object.set_source_game(SourceGame.Official)

    paint_object.to_parkobj("circus_paint.parkobj")

if __name__ == "__main__":
    generate_json()