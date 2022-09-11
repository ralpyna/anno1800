import os
import glob

class store:
    def __init__(self, name, coords_regions):
        self.name = name
        self.image = os.path.join('anno1800', 'images', 'store', name, 'id.png')
        self.image_states = self.register_states(self.name)
        
        self.region = self.register_region(name, coords_regions)

    def register_states(self, name):
        states = {}
        list_states = glob.glob(os.path.join('anno1800', 'images', 'store', name, 'states', '*.png'))
        for list_state in list_states:
            states[os.path.splitext(os.path.basename(list_state))[0]] = list_state
        return states

    def register_region(self, name, coords_regions):
        regions = {}
        for region in list(coords_regions['store'][name].keys()):
            regions[region] = coords_regions['store'][name][region]
        return regions
        