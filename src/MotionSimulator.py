from paint_struct.HeightSupportsTable import *
from paint_struct.PaintStruct import *
from paint_struct.PaintObjectFile import *
from paint_struct.Utils import *

def generate_height_support_tables(paint_object):
    height_supports = HeightSupportsTable()
    height_supports.height_offset = 128
    height_supports.id = "heightSupports_2x2"
    paint_object.add_height_support_table(height_supports)

def generate_vehicle_indices(paint_object):
    paint_object.set_vehicle_indices([0])

def generate_bound_boxes_structure(paint_object):
    track_sequences =   [1, 2, 3]
    offsets_x =          [16, -16, -16]
    offsets_y =          [-16, 16, -16]
    directions = list(range(4))

    bound_box_entry = BoundBoxEntry()
    bound_box_entry.id = "structure"
    for index in range(len(track_sequences)):
        track_sequence = track_sequences[index]
        offset_x = offsets_x[index]
        offset_y = offsets_y[index]

        for direction in directions:
            offset = Coords(offset_x, offset_y, 2)
            bb = BoundBox()

            if direction == 0:
                bb.offset = offset
                bb.length = Coords(20, 20, 44)
            elif direction == 1:
                bb.offset = offset
                bb.length = Coords(20, 20, 44)
            elif direction == 2:
                bb.offset = Coords(offset.x, offset.y + 5, offset.z)
                bb.length = Coords(20, 20, 44)
            elif direction == 3:
                bb.offset = Coords(offset.x + 5, offset.y, offset.z)
                bb.length = Coords(20, 20, 44)

            bb_value = BoundBoxEntryValue()
            bb_value.coords = offset
            bb_value.bound_box = bb
            bb_value.key.track_sequence = track_sequence
            bb_value.key.direction = direction
            bound_box_entry.add_value(bb_value)
    paint_object.add_bound_box(bound_box_entry)

def generate_bound_boxes_stairs(paint_object):
    track_sequences =   [1, 2, 3]
    offsets_x =          [16, -16, -16]
    offsets_y =          [-16, 16, -16]
    directions = list(range(4))

    bound_box_entry = BoundBoxEntry()
    bound_box_entry.id = "stairs"
    for index in range(len(track_sequences)):
        track_sequence = track_sequences[index]
        offset_x = offsets_x[index]
        offset_y = offsets_y[index]

        for direction in directions:
            offset = Coords(offset_x, offset_y, 2)
            bb = BoundBox()

            if direction == 0:
                bb.offset = offset
                bb.length = Coords(20, 20, 44)
            elif direction == 1:
                bb.offset = offset
                bb.length = Coords(20, 20, 44)
            elif direction == 2:
                bb.offset = Coords(offset.x, offset.y + 5, offset.z)
                bb.length = Coords(20, 20, 44)
            elif direction == 3:
                bb.offset = Coords(offset.x + 5, offset.y, offset.z)
                bb.length = Coords(20, 20, 44)

            bb_value = BoundBoxEntryValue()
            bb_value.coords = offset
            bb_value.bound_box = bb
            bb_value.key.track_sequence = track_sequence
            bb_value.key.direction = direction
            bound_box_entry.add_value(bb_value)
    paint_object.add_bound_box(bound_box_entry)

def generate_bound_boxes_stairs_rail(paint_object):
    track_sequences =   [1, 2, 3]
    offsets_x =          [16, -16, -16]
    offsets_y =          [-16, 16, -16]
    directions = list(range(4))

    bound_box_entry = BoundBoxEntry()
    bound_box_entry.id = "stairs_rail"
    for index in range(len(track_sequences)):
        track_sequence = track_sequences[index]
        offset_x = offsets_x[index]
        offset_y = offsets_y[index]

        for direction in directions:
            offset = Coords(offset_x, offset_y, 2)
            bb = BoundBox()

            if direction == 0:
                bb.offset = Coords(offset.x, offset.y + 32, offset.z)
                bb.length = Coords(20, 2, 44)
            elif direction == 1:
                bb.offset = Coords(offset.x + 34, offset.y, offset.z)
                bb.length = Coords(2, 20, 44)
            elif direction == 2:
                bb.offset = Coords(offset.x, offset.y - 10, offset.z)
                bb.length = Coords(20, 2, 44)
            elif direction == 3:
                bb.offset = Coords(offset.x - 10, offset.y, offset.z)
                bb.length = Coords(2, 20, 44)

            bb_value = BoundBoxEntryValue()
            bb_value.coords = offset
            bb_value.bound_box = bb
            bb_value.key.track_sequence = track_sequence
            bb_value.key.direction = direction
            bound_box_entry.add_value(bb_value)
    paint_object.add_bound_box(bound_box_entry)

def generate_bound_boxes(paint_object):
    generate_bound_boxes_structure(paint_object)
    generate_bound_boxes_stairs(paint_object)
    generate_bound_boxes_stairs_rail(paint_object)


def generate_image_id_offsets_structure(paint_object):
    structure_image = ImageIdOffset()
    structure_image.id = "structure"

    vehicle_restraints_positions = list(range(0, 256, 20))
    vehicle_restraints_positions.extend(list(range(255, 0, -20)))
    
    vehicle_pitches = list(range(35))
    vehicle_pitches.append(0xFF)
    for direction in range(4):
        for vehicle_pitch in vehicle_pitches:
            for vehicle_restraints_position in vehicle_restraints_positions:
                image_index = direction
                if vehicle_restraints_position >= 64:
                    image_index += (vehicle_restraints_position >> 6) << 2
                else:
                    image_index += vehicle_pitch * 4
                key = PaintStructKey()
                key.vehicle_pitch = vehicle_pitch
                key.direction = direction
                key.vehicle_restraints_position = vehicle_restraints_position

                values = [image_index]
                structure_image.add_entry(key, values)
    paint_object.add_image_id_offset(structure_image)

def generate_image_id_offsets_stairs(paint_object):
    stairs_image = ImageIdOffset()
    stairs_image.id = "stairs"

    for direction in range(4):
        key = PaintStructKey()
        key.direction = direction

        SprMotionSimulatorStairsR0 = 22154
        values = [SprMotionSimulatorStairsR0 + direction]
        stairs_image.add_entry(key, values)
    paint_object.add_image_id_offset(stairs_image)

def generate_image_id_offsets_stairs_rail(paint_object):
    stairs_rail_image = ImageIdOffset()
    stairs_rail_image.id = "stairs_rail"

    for direction in range(4):
        key = PaintStructKey()
        key.direction = direction

        SprMotionSimulatorStairsRailR0 = 22158
        values = [SprMotionSimulatorStairsRailR0 + direction]
        stairs_rail_image.add_entry(key, values)
    paint_object.add_image_id_offset(stairs_rail_image)

def generate_image_id_offsets(paint_object):
    generate_image_id_offsets_structure(paint_object)
    generate_image_id_offsets_stairs(paint_object)
    generate_image_id_offsets_stairs_rail(paint_object)

def generate_paint_structs_structure(direction):
    paint_struct = PaintStruct()
    paint_struct.image_id_scheme = Scheme.Misc
    paint_struct.image_id_base = ImageIdBase.Car0
    paint_struct.primary_colour = Colour.VehicleBody
    paint_struct.secondary_colour = Colour.VehicleTrim
    paint_struct.image_id_offset = "structure"
    paint_struct.boundbox_id = "structure"
    paint_struct.key.direction = direction
    if direction == 0:
        paint_struct.paint_type = PaintType.AddImageAsParent
    elif direction == 1:
        paint_struct.paint_type = PaintType.AddImageAsParent
    elif direction == 2:
        paint_struct.paint_type = PaintType.AddImageAsChild
    elif direction == 3:
        paint_struct.paint_type = PaintType.AddImageAsChild
    return paint_struct

def generate_paint_structs_stairs(direction):
    paint_struct = PaintStruct()
    paint_struct.image_id_scheme = Scheme.Misc
    paint_struct.primary_colour = Colour.VehicleBody
    paint_struct.secondary_colour = Colour.VehicleTrim
    paint_struct.image_id_offset = "stairs"
    paint_struct.boundbox_id = "stairs"
    paint_struct.key.direction = direction
    if direction == 0:
        paint_struct.paint_type = PaintType.AddImageAsChild
    elif direction == 1:
        paint_struct.paint_type = PaintType.AddImageAsChild
    elif direction == 2:
        paint_struct.paint_type = PaintType.AddImageAsParent
    elif direction == 3:
        paint_struct.paint_type = PaintType.AddImageAsParent
    return paint_struct

def generate_paint_structs_stairs_rail(direction):
    paint_struct = PaintStruct()
    paint_struct.image_id_scheme = Scheme.Misc
    paint_struct.primary_colour = Colour.VehicleBody
    paint_struct.secondary_colour = Colour.VehicleTrim
    paint_struct.image_id_offset = "stairs_rail"
    paint_struct.boundbox_id = "stairs_rail"
    paint_struct.key.direction = direction
    paint_struct.paint_type = PaintType.AddImageAsParent
    return paint_struct

def generate_paint_structs(paint_object):
    for direction in range(4):
        paint_struct_structure = generate_paint_structs_structure(direction)
        paint_struct_stairs = generate_paint_structs_stairs(direction)
        paint_struct_stairs_rail = generate_paint_structs_stairs_rail(direction)

        if direction == 0:
            paint_struct_structure.supports = SupportsType.WoodenA
            paint_struct_structure.supports_type = (direction & 1)
            paint_struct_structure.floor = FloorType.Cork
            paint_struct_structure.fences = FenceType.Ropes
            paint_object.add_paint_struct(paint_struct_structure)
            paint_object.add_paint_struct(paint_struct_stairs)
            paint_object.add_paint_struct(paint_struct_stairs_rail)
        elif direction == 1:
            paint_struct_structure.supports = SupportsType.WoodenA
            paint_struct_structure.supports_type = (direction & 1)
            paint_struct_structure.floor = FloorType.Cork
            paint_struct_structure.fences = FenceType.Ropes
            paint_object.add_paint_struct(paint_struct_structure)
            paint_object.add_paint_struct(paint_struct_stairs)
            paint_object.add_paint_struct(paint_struct_stairs_rail)
        elif direction == 2:
            paint_struct_stairs_rail.supports = SupportsType.WoodenA
            paint_struct_stairs_rail.supports_type = (direction & 1)
            paint_struct_stairs_rail.floor = FloorType.Cork
            paint_struct_stairs_rail.fences = FenceType.Ropes
            paint_object.add_paint_struct(paint_struct_stairs_rail)
            paint_object.add_paint_struct(paint_struct_stairs)
            paint_object.add_paint_struct(paint_struct_structure)
        elif direction == 3:
            paint_struct_stairs_rail.supports = SupportsType.WoodenA
            paint_struct_stairs_rail.supports_type = (direction & 1)
            paint_struct_stairs_rail.floor = FloorType.Cork
            paint_struct_stairs_rail.fences = FenceType.Ropes
            paint_object.add_paint_struct(paint_struct_stairs_rail)
            paint_object.add_paint_struct(paint_struct_stairs)
            paint_object.add_paint_struct(paint_struct_structure)
    supports = PaintStruct()
    supports.height_supports = "heightSupports_2x2"
    paint_object.add_paint_struct(supports)


def generate_key_range(paint_object):
    vehicle_pitch = list(range(35))
    vehicle_pitch.append(0xFF)

    vehicle_restraints_positions = list(range(0, 256, 20))
    vehicle_restraints_positions.extend(list(range(255, 0, -20)))

    direction = list(range(4))
    track_sequences = list(range(4))

    key_range = PaintStructKeyRange()
    key_range.TrackSequences = track_sequences
    key_range.VehiclePitches = vehicle_pitch
    key_range.Directions = direction
    key_range.VehicleRestraintsPositions = vehicle_restraints_positions
    paint_object.set_key_range(key_range)
        

def generate():
    paint_object = PaintObjectFile()
    paint_object.add_author("OpenRCT2 Developpers")
    paint_object.set_object_id("openrct2.paint.motsim")
    paint_object.set_source_game("official")
    paint_object.set_object_version("1.0")
    
    generate_key_range(paint_object)
    generate_height_support_tables(paint_object)
    generate_vehicle_indices(paint_object)
    generate_bound_boxes(paint_object)
    generate_image_id_offsets(paint_object)
    generate_paint_structs(paint_object)

    paint_object.to_json("motion_simulator.json")
    paint_object.to_parkobj("motion_simulator.parkobj")

if __name__ == "__main__":
    generate()

#vehiclePitch=[0-31]
#vehcileRestraintsPosition=[0-255]