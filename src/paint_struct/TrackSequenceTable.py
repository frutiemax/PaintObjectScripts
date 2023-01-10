from paint_struct.TrackElement import *
class TrackSequenceTable:
    def __init__(self):
        self.trackElement = TrackElement.FlatTrack3x3
        self.sequences = []
    
    def to_dict(self):
        return { "trackElement": self.trackElement, "sequences": self.sequences }