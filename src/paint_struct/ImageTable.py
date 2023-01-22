class Scheme:
    Misc = "misc"
    Track = "track"

class ColourType:
    VehicleBody = "vehicleBody"
    VehicleTrim = "vehicleTrim"
    PeepTShirt = "peepTShirt"

class Colour:
    def __init__(self):
        self.type = None
        self.index = 0
    
    def to_dict(self):
        return {"colourType": self.type, "colourIndex": self.index}

class ImageProperties:
    def __init__(self):
        self.primary_colour = None
        self.secondary_colour = None
        self.scheme = None
        self.offset = None

    def set_primary_colour(self, colour):
        self.primary_colour = colour.to_dict()
    
    def set_secondary_colour(self, colour):
        self.secondary_colour = colour.to_dict()
    
    def to_dict(self):
        result = {}
        
        if self.primary_colour != None:
            result["primaryColour"] = self.primary_colour
        
        if self.secondary_colour != None:
            result["secondaryColour"] = self.secondary_colour

        if self.scheme != None:
            result["scheme"] = self.scheme
        
        if self.offset != None:
            result["offset"] = self.offset
        return result

class Image:
    def __init__(self):
        self.key = None
        self.properties = []
    
    def add_properties(self, prop):
        self.properties.append(prop.to_dict())
    
    def set_key(self, key):
        self.key = key.to_dict()

    def to_dict(self):
        result = self.key
        result["properties"] = self.properties
        return result

class ImageTable:
    def __init__(self):
        self.id = ""
        self.images = []
    
    def add_image(self, image):
        dict = image.to_dict()
        self.images.append(dict)

    def to_dict(self):
        return {"id": self.id, "images": self.images}