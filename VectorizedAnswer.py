class VectorizedAnswer:
    def __init__(self, line, vec):
        self.line = line
        self.vec = vec

    def __str__(self):
        return self.line

    def __repr__(self):
        return str(self)