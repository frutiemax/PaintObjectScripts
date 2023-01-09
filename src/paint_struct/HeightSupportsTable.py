class HeightSupportsSegment:
    def __init__(self, track_sequence, values):
        self.track_sequence = track_sequence
        self.values = values
    
    def to_dict(self):
        return {"trackSequence": self.track_sequence, "values": self.values}

class HeightSupportsTable:
    def __init__(self):
        self.id = ""
        self.height_offset = 0
        self.segments = []
    
    def add_support_segment(self, height_support_segment):
        self.segments.append(height_support_segment.to_dict())
    
    def to_dict(self):
        return {"id": self.id, "heightOffset": self.height_offset, "segments": self.segments}