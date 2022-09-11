import pyautogui as pag
import logging as log
import os

class detect:
    def __init__(self
                , file_targets
                , search_region=False
                , search_all_screen=False
                , threshold_conf=0.97):
        self.file_targets = file_targets if isinstance(file_targets, list) else [file_targets]

        if search_all_screen:
            from PIL import ImageGrab
            from functools import partial
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if not search_region == False:
            self.search_region = [search_region[0]
                                , search_region[1]
                                , search_region[2] - search_region[0]
                                , search_region[3] - search_region[1]]
        else:
            width, height = pag.size()
            self.search_region = [0, 0, width, height]

        self.threshold_conf = threshold_conf

    def get_coords(self):
        results = []
        for file_target in self.file_targets:
            searched_target = pag.locateAllOnScreen(file_target
                                                    , confidence=self.threshold_conf
                                                    , region=self.search_region)
            for detected_coords in list(searched_target):
                center_point = pag.center(detected_coords)
                results.append([os.path.splitext(os.path.basename(file_target))[0], center_point.x, center_point.y])

        return results

    def find(self):
        for file_target in self.file_targets:
            searched_target = pag.locateAllOnScreen(file_target
                                                    , confidence=self.threshold_conf
                                                    , region=self.search_region)
            if len(list(searched_target)) > 0:
                return True

        return False

class detects:
    def __init__(self
                , file_targets
                , search_all_screen=False
                , search_region=False
                , threshold_conf=0.97):
        self.file_targets = file_targets if isinstance(file_targets, list) else [file_targets]

        if search_all_screen:
            from PIL import ImageGrab
            from functools import partial
            ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)

        if not search_region == False:
            self.search_region = [search_region[0]
                                , search_region[1]
                                , search_region[2] - search_region[0]
                                , search_region[3] - search_region[1]]
        else:
            width, height = pag.size()
            self.search_region = [0, 0, width, height]

        self.threshold_conf = threshold_conf

    def get_coords(self):
        results = []
        for file_target in self.file_targets:
            searched_target = pag.locateAllOnScreen(file_target
                                                    , confidence=self.threshold_conf
                                                    , region=self.search_region)
            for detected_coords in list(searched_target):
                center_point = pag.center(detected_coords)
                results.append([file_target, center_point.x, center_point.y])

        return results

    def find(self):
        for file_target in self.file_targets:
            searched_target = pag.locateAllOnScreen(file_target
                                                    , confidence=self.threshold_conf
                                                    , region=self.search_region)
            if len(list(searched_target)) > 0:
                return True

        return False
