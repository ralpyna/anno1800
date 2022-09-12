import pyautogui as pag
import time
import logging as log

class windows:
    def __init__(self, win_name, coords_buttons):
        self.win_name = win_name
        self.coords_buttons = coords_buttons 
    
    def check_active_window(self):
        current_win_info = pag.getActiveWindow()
        if not current_win_info == None:
            if self.win_name == current_win_info.title:
                return True
        return False

    def click_button(self, category, button, delay=0.2, wait_active_winow=True):
        time.sleep(delay)
        while True:          
            if self.check_active_window():
                pag.click(self.coords_buttons[category][button])
                break
            log.debug('waiting for window of application...')
            time.sleep(delay)

    def click(self, coords, delay=0.2, wait_active_winow=True):
        time.sleep(delay)
        while True:
            if self.check_active_window():
                pag.click(coords)
                break
            log.debug('waiting for window of application...')
            time.sleep(delay)