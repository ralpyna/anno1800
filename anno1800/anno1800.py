import logging as log
import os
import json
import pyautogui as pag
import glob

from anno1800.item import item
from anno1800.store import store
from anno1800.facility import facility
from anno1800.windows import windows

class anno1800:
    def __init__(self, win_name='Anno 1800'):
        self.items = self.register_items()
        self.stores = self.register_stores(self.get_def_coords('regions'))
        self.facilities = self.register_facilities(self.get_def_coords('regions'))
        self.windows = windows(win_name, self.get_def_coords('buttons'))
        # print(self.items['test'].id)
        # print(self.stores['equipments'].id_states['no_inventory'])

    def register_items(self):
        items = {}
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'items', '*'))
        for list_dir in list_dirs:
            list_images = glob.glob(os.path.join(list_dir, '*.png'))
            for list_image in list_images:
                name_item = os.path.splitext(os.path.basename(list_image))[0]
                items[name_item] = item(os.path.dirname(list_image).split(os.path.sep)[-1], name_item)
        return items

    def is_item(self, item, type=None):
        if type == None:
            list_dirs = glob.glob(os.path.join('anno1800', 'images', 'items', '*'))
        elif self.is_store(type):
            list_dirs = glob.glob(os.path.join('anno1800', 'images', 'items', type))
        else:
            log.error('invalid the type: ' + type)

        for list_dir in list_dirs:
            list_images = glob.glob(os.path.join(list_dir, '*.png'))
            for list_image in list_images:
                name_item = os.path.splitext(os.path.basename(list_image))[0]
                if item == name_item:
                    return True
        return False

    def register_stores(self, coords_regions):
        stores = {}
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'stores', '*'))
        for list_dir in list_dirs:
            name_store = os.path.splitext(os.path.basename(list_dir))[0]
            stores[name_store] = store(name_store, coords_regions)
        return stores
    
    def is_store(self, store):
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'stores', '*'))
        for list_dir in list_dirs:
            name_store = os.path.splitext(os.path.basename(list_dir))[0]
            if store == name_store:
                return True
        return False
    
    def register_facilities(self, coords_regions):
        facilities = {}
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'facilities', '*'))
        for list_dir in list_dirs:
            name_facility = os.path.splitext(os.path.basename(list_dir))[0]
            facilities[name_facility] = facility(name_facility, coords_regions)
        return facilities
    
    def is_facility(self, facility):
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'facilities', '*'))
        for list_dir in list_dirs:
            name_facility = os.path.splitext(os.path.basename(list_dir))[0]
            if facility == name_facility:
                return True
        return False

    def get_def_coords(self, type_coords):
        file_coords = os.path.join('anno1800', 'coords', type_coords + '.json')
        with open(file_coords, 'r') as file_json:
            coords = json.load(file_json)
        return coords

    def format_items(self, items, type=None):
        if not isinstance(items, list):
            log.error('invalid the format: isinstance=' + isinstance(items, list))
        
        valid_items = []
        if items[0] == '*':
            list_items = self.items
            for list_item in list_items:
                if self.is_item(list_item, type):
                    valid_items.append(self.items[list_item].image)
        else:
            for item in items:
                if self.is_item(item, type):
                    valid_items.append(self.items[item].image)

        return valid_items
            
        
