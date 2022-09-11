import pyautogui as pag
import logging as log
import os

from anno1800.detect import detect

class wishlist:
    wishlist = []
        
    def add_stuff_wishlist(self, stuff):
        if self.anno1800.check_valid_stuff(self.type_store, stuff):
            if not self.is_stuff_wishlist(stuff):
                self.wishlist.append(stuff)

    def delete_stuff_wishlist(self, stuff):
        if self.is_stuff_wishlist(stuff):
            self.wishlist.remove(stuff)

    def get_wishlist(self, stuff):
        return self.wishlist

    def is_stuff_wishlist(self, stuff):
        if stuff in self.wishlist:
            return True


class store(wishlist):
    def __init__(self, anno1800, type_store):
        self.anno1800 = anno1800
        self.type_store = self.check_valid_type_store(type_store)

        self.det_store_screen = detect(anno1800.get_file_stuff(self.type_store, 'id'), search_region=self.anno1800.coords_commons['id']['store'])

    def check_valid_type_store(self, type_store):
        if type_store in self.anno1800.type_stores:
            return type_store 
        else:
            log.critical(type_store)

    def buy_stuff(self, stuff):
        if
        self.anno1800.win.click_button('trade_in_ship')


