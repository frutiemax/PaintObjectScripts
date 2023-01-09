
class TrackSequenceTable:
    def __init__(self):
        self.id = ""
        self.sequences = []
    
    def to_dict(self):
        return { "id": self.id, "sequences": self.sequences }