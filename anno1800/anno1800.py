import logging as log
log.basicConfig(
    format='[%(levelname)s] %(funcName)s:%(lineno)d: %(message)s'
    #format='%(asctime)s %(levelname): %(funcName)s:%(lineno)d: %(message)s',
    #datefmt='%m/%d/%Y %I:%M:%S %p',
)
import os
import json
import pyautogui as pag
import glob

from anno1800.item import item
from anno1800.store import store
from anno1800.windows import windows

class anno1800:
    def __init__(self, win_name='Anno 1800'):
        self.items = self.register_items()
        self.stores = self.register_stores(self.get_def_coords('regions'))
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

    def is_item(self, item):
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'items', '*'))
        for list_dir in list_dirs:
            list_images = glob.glob(os.path.join(list_dir, '*.png'))
            for list_image in list_images:
                name_item = os.path.splitext(os.path.basename(list_image))[0]
                if item == name_item:
                    return True
        return False

    def register_stores(self, coords_regions):
        stores = {}
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'store', '*'))
        for list_dir in list_dirs:
            name_store = os.path.splitext(os.path.basename(list_dir))[0]
            stores[name_store] = store(name_store, coords_regions)
        return stores
    
    def is_store(self, store):
        list_dirs = glob.glob(os.path.join('anno1800', 'images', 'store', '*'))
        for list_dir in list_dirs:
            name_store = os.path.splitext(os.path.basename(list_dir))[0]
            if store == name_store:
                return True
        return False

    def get_def_coords(self, type_coords):
        file_coords = os.path.join('anno1800', 'coords', type_coords + '.json')
        with open(file_coords, 'r') as file_json:
            coords = json.load(file_json)
        return coords
        
