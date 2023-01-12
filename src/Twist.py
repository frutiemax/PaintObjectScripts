from paint_struct.PaintStruct import *
from paint_struct.PaintObjectFile import *
from paint_struct.HeightSupportsTable import *
from paint_struct.TrackElement import *
from paint_struct.Coords import *
from paint_struct.BoundBox import *
from paint_struct.TrackSequenceTable import *
from paint_struct.EdgeTable import *

def paint_twist_structure(paint_object, track_element, direction, xOffset, yOffset, vehicle_num_peeps, track_sequence):
    #paint the structure first
    paintStruct = PaintStruct()
    paintStruct.key.element = TrackElement.FlatTrack3x3
    paintStruct.key.track_sequence = track_sequence
    paintStruct.key.direction = direction
    paintStruct.paint_type = PaintType.AddImageAsParent
    paintStruct.image_id_base = ImageIdBase.Car0
    paintStruct.key.element = track_element
    paintStruct.image_id_offset = "structure"

    paintStruct.offset = Coords(xOffset, yOffset, 7)
    paintStruct.boundbox = BoundBox(Coords(xOffset + 16, yOffset + 16, 7), Coords(24, 24, 48))
    paintStruct.primary_colour = Colour.VehicleBody
    paintStruct.secondary_colour = Colour.VehicleTrim
    paintStruct.primary_colour_index = 0
    paintStruct.secondary_colour_index = 0
    paintStruct.image_id_scheme = Scheme.Misc
    paintStruct.key.vehicle_index = 0
    paint_object.add_paint_struct(paintStruct)

    #peeps
    paintStruct.key.vehicle_num_peeps = vehicle_num_peeps
    paintStruct.primary_colour = Colour.PeepTShirt
    paintStruct.secondary_colour = Colour.PeepTShirt

    index = 0
    for i in range(0, vehicle_num_peeps, 2):
        paintStruct.primary_colour_index = i
        paintStruct.secondary_colour_index = i + 1
        paintStruct.image_id_offset_index = index
        paintStruct.image_id_offset = "peep"
        paintStruct.paint_type = PaintType.AddImageAsChild
        paint_object.add_paint_struct(paintStruct)
        index = index + 1

def paint_twist(paint_object, track_element, direction, vehicle_num_peeps, track_sequence):
    track_sequence = TrackMap3x3[direction][track_sequence]
    if track_sequence == 1:
        paint_twist_structure(paint_object, track_element, direction, 32, 32, vehicle_num_peeps, track_sequence)
    elif track_sequence == 3:
        paint_twist_structure(paint_object, track_element, direction, 32, -32, vehicle_num_peeps, track_sequence)
    elif track_sequence == 5:
        paint_twist_structure(paint_object, track_element, direction, 0, -32, vehicle_num_peeps, track_sequence)
    elif track_sequence == 6:
        paint_twist_structure(paint_object, track_element, direction, -32, 32, vehicle_num_peeps, track_sequence)
    elif track_sequence == 7:
        paint_twist_structure(paint_object, track_element, direction, -32, -32, vehicle_num_peeps, track_sequence)
    elif track_sequence == 8:
        paint_twist_structure(paint_object, track_element, direction, -32, 0, vehicle_num_peeps, track_sequence)

def calculate_structure_image_id(direction, vehicle_sprite_direction, vehicle_pitch):
    frameNum = (direction % 88) % 216
    frameNum += (vehicle_sprite_direction >> 3) << 4
    frameNum += vehicle_pitch
    frameNum = frameNum % 216
    structureFrameNum = frameNum % 24
    return [structureFrameNum]

def calculate_peep_image_id(direction, vehicle_sprite_direction, vehicle_pitch, vehicle_num_peeps):
    result = []

    frameNum = (direction % 88) % 216
    frameNum += (vehicle_sprite_direction >> 3) << 4
    frameNum += vehicle_pitch
    frameNum = frameNum % 216

    for i in range(0, vehicle_num_peeps, 2):
        peep_frame_num = (frameNum + i * 12) % 216
        result.append(24 + peep_frame_num)
    return result

def generate_json():
    
    track_sequences = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    directions = [0, 1, 2, 3]
    track_element = TrackElement.FlatTrack3x3
    vehicle_pitch_values = list(range(216))
    vehicle_sprite_direction_values = [0, 8, 16, 24]
    vehicle_num_peeps_values = list(range(19))

    paint_object = PaintObjectFile()

    #floor + fences + supports
    base_paint_struct = PaintStruct()
    base_paint_struct.edges = "edges_3x3"
    base_paint_struct.supports = SupportsType.WoodenA
    base_paint_struct.image_id_scheme = Scheme.Misc
    base_paint_struct.floor = FloorType.Cork
    base_paint_struct.fences = FenceType.Ropes
    base_paint_struct.element = track_element
    paint_object.add_paint_struct(base_paint_struct)
    
    #generate single keys
    for arg in track_sequences:
        singleKey = PaintStruct()
        singleKey.key.track_sequence = arg
        paint_object.add_paint_struct(singleKey)
    noPeepKey = PaintStruct()
    noPeepKey.key.vehicle_num_peeps = 0
    paint_object.add_paint_struct(noPeepKey)

    #generate all the possible combinations to pass through the paint function
    #we only need the peep_num variable for the loop
    args = [[paint_object, track_element, direction, vehicle_num_peeps, track_sequence]
        for track_sequence in track_sequences
        for direction in directions
        for vehicle_num_peeps in vehicle_num_peeps_values]

    for arg in args:
        paint_twist(arg[0], arg[1], arg[2], arg[3], arg[4])
    
    #height supports
    height_supports = PaintStruct()
    height_supports.key.element = track_element
    height_supports.paint_type = PaintType.SetSegmentsSupportsHeight
    height_supports.height_supports = "heightSupports_3x3"
    paint_object.add_paint_struct(height_supports)

    #track sequence table
    sequenceTable = TrackSequenceTable()
    sequenceTable.trackElement = TrackElement.FlatTrack3x3
    sequenceTable.sequences = TrackMap3x3
    paint_object.add_sequence_table(sequenceTable)

    #edge tables
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
    
    #height support tables
    height_supports = HeightSupportsTable()
    height_supports.height_offset = 128
    height_supports.add_support_segment(HeightSupportsSegment(1, [Segment.B4, Segment.C8, Segment.CC]))
    height_supports.add_support_segment(HeightSupportsSegment(3, [Segment.CC, Segment.BC, Segment.D4]))
    height_supports.add_support_segment(HeightSupportsSegment(6, [Segment.C8, Segment.B8, Segment.D0]))
    height_supports.add_support_segment(HeightSupportsSegment(7, [Segment.D0, Segment.C0, Segment.D4]))
    height_supports.id = "heightSupports_3x3"
    paint_object.add_height_support_table(height_supports)

    #imageIdOffsets
    #we need the direction, vehicle_sprite_direction, vehicle_pitch
    structureImageId = ImageIdOffset()
    structureImageId.id = "structure"
    args = [[direction, vehicle_sprite_direction, vehicle_pitch]
        for direction in directions
        for vehicle_sprite_direction in vehicle_sprite_direction_values
        for vehicle_pitch in vehicle_pitch_values]
    for arg in args:
        values = calculate_structure_image_id(arg[0], arg[1], arg[2])
        key = PaintStructKey()
        key.direction = arg[0]
        key.vehicle_sprite_direction = arg[1]
        key.vehicle_pitch = arg[2]
        structureImageId.add_entry(key, values)
    paint_object.add_image_id_offset(structureImageId)

    #we need the direction, vehicle_sprite_direction, vehicle_pitch, vehicle_num_peeps
    peepImageId = ImageIdOffset()
    peepImageId.id = "peep"
    args = [[direction, vehicle_sprite_direction, vehicle_pitch, vehicle_num_peeps_values[-1]]
        for direction in directions
        for vehicle_sprite_direction in vehicle_sprite_direction_values
        for vehicle_pitch in vehicle_pitch_values]
        #for vehicle_num_peeps in vehicle_num_peeps_values]
    for arg in args:
        values = calculate_peep_image_id(arg[0], arg[1], arg[2], arg[3])
        if len(values) == 0:
            continue
        key = PaintStructKey()
        key.direction = arg[0]
        key.vehicle_sprite_direction = arg[1]
        key.vehicle_pitch = arg[2]
        #key.vehicle_num_peeps = arg[3]
        peepImageId.add_entry(key, values)
    paint_object.add_image_id_offset(peepImageId)
    paint_object.set_vehicle_indices([0])

    paint_object.set_object_id("openrct2.paint.twist")
    paint_object.set_object_version("1.0")
    paint_object.add_author("OpenRCT2 Developpers")
    paint_object.set_source_game(SourceGame.Official)

    paint_object.to_json("twist_paint.json")
    paint_object.to_parkobj("twist_paint.parkobj")

if __name__ == "__main__":
    generate_json()