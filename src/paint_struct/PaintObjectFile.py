import json
import zipfile

class SourceGame:
    Official = "official"
    Custom = "custom"

class PaintObjectFile:
    def __init__(self):
        self.paint_structs = []
        self.sequence_tables = []
        self.edge_tables = []
        self.height_tables = []
        self.imageIdOffsets = []
        self.vehicleIndices = []
        self.id = ""
        self.version = ""
        self.authors = []
        self.object_type = "paint"
        self.source_game = "official"
    
    def add_sequence_table(self, sequence_table):
        self.sequence_tables.append(sequence_table.to_dict())
    
    def add_edge_table(self, edge_table):
        self.edge_tables.append(edge_table.to_dict())
    
    def add_height_support_table(self, height_table):
        self.height_tables.append(height_table.to_dict())
    
    def add_image_id_offset(self, image_id_offset):
        self.imageIdOffsets.append(image_id_offset.to_dict())

    def set_vehicle_indices(self, vehicle_indices):
        self.vehicleIndices = vehicle_indices
    
    def add_paint_struct(self, paint_struct):
        dict = paint_struct.to_dict()

        #check if it already exists
        count = self.paint_structs.count(dict)
        if count == 0:
            self.paint_structs.append(paint_struct.to_dict())
    
    def set_object_id(self, object_id):
        self.id = object_id
    
    def set_object_version(self, version):
        self.version = version
    
    def add_author(self, author):
        self.authors.append(author)
    
    def set_source_game(self, source_game):
        self.source_game = source_game
    
    def to_json(self, filename):
        #dump the object properties first
        result = ""
        dict = {"id": self.id, "version": self.version, "authors": self.authors,
            "objectType": self.object_type, "sourceGame": self.source_game}
        
        dict["trackSequenceTables"] = self.sequence_tables
        dict["edgesTables"] = self.edge_tables
        dict["heightSupportsTables"] = self.height_tables
        dict["imageIdOffsets"] = self.imageIdOffsets
        dict["vehicleIndices"] = self.vehicleIndices
        dict["paintStructs"] = self.paint_structs
        result += json.dumps(dict, indent=4)

        #output to the given file
        file = open(filename, "w")
        file.write(result)
        file.close()
    
    def to_parkobj(self, filename):
        self.to_json('object.json')

        with zipfile.ZipFile(filename, mode='w', compression=zipfile.ZIP_DEFLATED) as myzip:
            myzip.write('object.json')
    
