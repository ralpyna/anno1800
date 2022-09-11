import os

class item:
    def __init__(self, type, name):
        self.name = name
        self.type = type
        self.image = os.path.join('anno1800', 'images', 'items', type, name + '.png')