import pyautogui as pag
import time

class windows:
    def __init__(self, win_name, coords_buttons):
        self.win_name = win_name
        self.coords_buttons = coords_buttons 
    
    def check_active_window(self):
        if self.win_name == pag.getActiveWindow().title:
            return True
        return False

    def click_button(self, button, delay=0.2):
        time.sleep(delay)
        if self.check_active_window():
            pag.click(self.coords_buttons['trade_in_ship'])