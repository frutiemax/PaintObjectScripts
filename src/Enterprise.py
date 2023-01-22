from paint_struct.HeightSupportsTable import *
from paint_struct.PaintStruct import *
from paint_struct.PaintObjectFile import *
from paint_struct.Utils import *

def generate_height_support_tables(paint_object):
    height_supports = HeightSupportsTable()
    height_supports.height_offset = 128
    height_supports.add_support_segment(HeightSupportsSegment(0, [Segment.B4, Segment.C8, Segment.CC]))
    height_supports.add_support_segment(HeightSupportsSegment(3, [Segment.CC, Segment.BC, Segment.D4]))
    height_supports.add_support_segment(HeightSupportsSegment(12, [Segment.C8, Segment.B8, Segment.D0]))
    height_supports.add_support_segment(HeightSupportsSegment(15, [Segment.D0, Segment.C0, Segment.D4]))
    height_supports.id = "heightSupports_4x4"
    paint_object.add_height_support_table(height_supports)

def generate_vehicle_indices(paint_object):
    paint_object.set_vehicle_indices([0])

def generate_bound_boxes(paint_object):
    track_sequences =   [5,     6,      10,     9,      0,      3,      15,         12,     7,      11,     14,     13]
    offsets_x =          [16,    16,     -16,    -16,    48,     48,     -48,        -48,    16,     -16,    -48,    -48]
    offsets_y =          [16,    -16,    -16,    16,     48,     -48,    -48,        48,     -48,    -48,    -16,    16]

    bound_box_entry = BoundBoxEntry()
    bound_box_entry.id = "bb"
    for index in range(len(track_sequences)):
        track_sequence = track_sequences[index]
        offset_x = offsets_x[index]
        offset_y = offsets_y[index]

        offset = Coords(offset_x, offset_y, 7)
        bb = BoundBox(Coords(0, 0, 7), Coords(24, 24, 48))
        bb_value = BoundBoxEntryValue()
        bb_value.coords = offset
        bb_value.bound_box = bb
        bb_value.key.track_sequence = track_sequence
        bound_box_entry.add_value(bb_value)
    paint_object.add_bound_box(bound_box_entry)

def generate_image_id_offsets_structure(structure_image_id, session_current_rotation, vehicle_pitch, vehicle_sprite_direction):
    image_offset = Utils.get_direction_with_offset(session_current_rotation)
    image_offset = (vehicle_pitch << 2) + (((vehicle_sprite_direction >> 3) + session_current_rotation) % 4)

    key = PaintStructKey()
    key.vehicle_sprite_direction = vehicle_sprite_direction
    key.vehicle_pitch = vehicle_pitch
    key.session_current_rotation = session_current_rotation
    structure_image_id.add_entry(key, [image_offset])


def generate_image_id_offsets_peeps(peep_image_id, session_current_rotation, vehicle_pitch, vehicle_sprite_direction, vehicle_num_peeps):
    image_offset = Utils.get_direction_with_offset(session_current_rotation)
    image_offset = (vehicle_pitch << 2) + (((vehicle_sprite_direction >> 3) + session_current_rotation) % 4)
    key = PaintStructKey()
    key.vehicle_sprite_direction = vehicle_sprite_direction
    key.vehicle_pitch = vehicle_pitch
    key.session_current_rotation = session_current_rotation
    key.vehicle_num_peeps = vehicle_num_peeps
    if image_offset >= 12:
        return
    
    values = []
    for i in range(15):
        if vehicle_num_peeps <= i:
            break
        frame_offset_1 = ((image_offset % 4) * 4 + (i * 4) % 15) & 0x0F
        frame_offset_2 = Utils.floor2(image_offset, 4) * 4
        values.append(196 + frame_offset_1 + frame_offset_2)
    peep_image_id.add_entry(key, values)

def generate_image_id_offsets(paint_object):
    #image id of structure is dependant on Session.CurrentRotation, vehiclePitch, vehicleSpriteDirection
    #image id of peeps is dependant on Session.CurrentRotation, vehiclePitch, vehicleSpriteDirection, vehicleNumPeeps
    session_current_rotations = [0, 1, 2, 3]
    vehicle_pitches = range(49)
    vehicle_sprite_directions = [0, 8, 16, 24]
    vehicle_num_peepes = range(17)

    structure_image_id = ImageIdOffset()
    structure_image_id.id = "structure"

    args = [[structure_image_id, session_current_rotation, vehicle_pitch, vehicle_sprite_direction]
        for session_current_rotation in session_current_rotations
        for vehicle_pitch in vehicle_pitches
        for vehicle_sprite_direction in vehicle_sprite_directions]
    for arg in args:
        generate_image_id_offsets_structure(arg[0], arg[1], arg[2], arg[3])
    paint_object.add_image_id_offset(structure_image_id)

    peeps_image_id = ImageIdOffset()
    peeps_image_id.id = "peeps"
    args = [[peeps_image_id, session_current_rotation, vehicle_pitch, vehicle_sprite_direction, vehicle_num_peeps]
        for session_current_rotation in session_current_rotations
        for vehicle_pitch in vehicle_pitches
        for vehicle_sprite_direction in vehicle_sprite_directions
        for vehicle_num_peeps in vehicle_num_peepes]
    for arg in args:
        generate_image_id_offsets_peeps(arg[0], arg[1], arg[2], arg[3], arg[4])
    paint_object.add_image_id_offset(peeps_image_id)

def generate_paint_structs(paint_object):
    paint_struct = PaintStruct()

    num_peepes = range(0,49)
    session_current_rotations = range(4)
    vehicle_pitches = range(49)
    vehicle_sprite_directions = [0, 8, 16, 24]

    paint_struct.supports = SupportsType.WoodenA
    paint_struct.image_id_scheme = Scheme.Misc
    paint_struct.floor = FloorType.Cork
    paint_struct.fences = FenceType.Ropes
    paint_struct.key.vehicle_num_peeps = None
    paint_struct.key.element = TrackElement.FlatTrack4x4
    paint_struct.image_id_base = ImageIdBase.Car0
    paint_struct.primary_colour = Colour.VehicleBody
    paint_struct.secondary_colour = Colour.VehicleTrim
    paint_struct.image_id_offset = "structure"
    paint_struct.boundbox_id = "bb"
    paint_struct.image_id_offset_index = 0
    paint_struct.paint_type = PaintType.AddImageAsParent
    paint_object.add_paint_struct(paint_struct)

    for session_current_rotation in session_current_rotations:
        for vehicle_pitch in vehicle_pitches:
            for vehicle_sprite_direction in vehicle_sprite_directions:
                for num_peeps in num_peepes:
                    paint_struct.supports = SupportsType.WoodenA
                    paint_struct.supports_type = (int(session_current_rotation / 8) & 1)
                    paint_struct.image_id_scheme = Scheme.Misc
                    paint_struct.floor = FloorType.Cork
                    paint_struct.fences = FenceType.Ropes
                    paint_struct.key.element = TrackElement.FlatTrack4x4
                    paint_struct.image_id_base = ImageIdBase.Car0
                    paint_struct.primary_colour = Colour.VehicleBody
                    paint_struct.secondary_colour = Colour.VehicleTrim
                    paint_struct.image_id_offset = "structure"
                    paint_struct.boundbox_id = "bb"
                    paint_struct.image_id_offset_index = 0
                    paint_struct.paint_type = PaintType.AddImageAsParent
                    paint_struct.key.vehicle_num_peeps = num_peeps
                    paint_struct.key.vehicle_pitch = vehicle_pitch
                    #paint_object.add_paint_struct(paint_struct)

                    paint_struct.image_id_offset = "peeps"
                    paint_struct.primary_colour = Colour.PeepTShirt
                    paint_struct.secondary_colour = None
                    paint_struct.height_supports = None
                    paint_struct.paint_type = PaintType.AddImageAsChild
                    paint_struct.floor = None
                    paint_struct.fences = None
                    paint_struct.supports = None

                    #we need to calculate this as this is an exit parameter...
                    image_offset = Utils.get_direction_with_offset(session_current_rotation)
                    image_offset = (vehicle_pitch << 2) + (((vehicle_sprite_direction >> 3) + session_current_rotation) % 4)

                    if image_offset >= 12:
                        continue

                    for i in range(15):
                        if num_peeps <= i:
                            break
                        paint_struct.image_id_offset_index = i
                        paint_object.add_paint_struct(paint_struct)
                    
    #generate a last paint struct for the supports
    supports = PaintStruct()
    supports.height_supports = "heightSupports_4x4"
    paint_object.add_paint_struct(supports)

def generate_key_range(paint_object):
    num_peepes = [i for i in range(0,49)]
    session_current_rotations = [i for i in range(4)]
    vehicle_pitches = [i for i in range(49)]
    vehicle_sprite_directions = [0, 8, 16, 24]

    key_range = PaintStructKeyRange()
    key_range.VehicleNumPeeps = num_peepes
    key_range.SessionCurrentRotations = session_current_rotations
    key_range.VehiclePitches = vehicle_pitches
    key_range.VehicleSpriteDirections = vehicle_sprite_directions
    paint_object.set_key_range(key_range)
        

def generate():
    paint_object = PaintObjectFile()
    paint_object.add_author("OpenRCT2 Developpers")
    paint_object.set_object_id("openrct2.paint.entpr")
    paint_object.set_source_game("official")
    paint_object.set_object_version("1.0")
    
    generate_key_range(paint_object)
    generate_height_support_tables(paint_object)
    generate_vehicle_indices(paint_object)
    generate_bound_boxes(paint_object)
    generate_image_id_offsets(paint_object)
    generate_paint_structs(paint_object)

    paint_object.to_json("enterprise.json")
    paint_object.to_parkobj("enterprise.parkobj")

if __name__ == "__main__":
    generate()

'''
VehiclePitch
0-48

VehicleSpriteDirection
0, 8, 16, 24

SessionCurrentRotation
2
3
0
1

VehicleNumPeeps
0-16



'''