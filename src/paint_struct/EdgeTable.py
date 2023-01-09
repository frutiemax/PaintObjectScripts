
class EdgeTable:
    def __init__(self):
        self.id = ""
        self.edges = []
    
    def to_dict(self):
        return { "id": self.id, "edges": self.edges }