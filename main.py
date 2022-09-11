
from anno1800.anno1800 import anno1800
import pyautogui as pag
import multiprocessing as mltprocess
import keyboard
import time
import os
import argparse
from logger import log

# from anno1800.store import store
# pyautogui.move(200, 200, 2)

def auto_buy(items, type_store):
    from anno1800.anno1800 import anno1800
    from anno1800.detect import detect

    log.debug('items=[' + ','.join(items) + '] | type_store=' + type_store)

    anno1800 = anno1800()

    list_items = []
    if items[0] == '*':
        list_items = anno1800.items
    else:
        for item in items:
            list_items.append(anno1800.items[item].image)

    det_items = detect(list_items
                    , anno1800.stores[type_store].region['list_items'])
    det_store = detect(anno1800.stores[type_store].image
                    , anno1800.stores[type_store].region['store'])

    while(True):
        time.sleep(3)
        log.debug(list_items)

class multiprocess:
    def __init__(self, args, daemon=True):
        self.flag_started = False
        self.flag_dead = False
        self.name = args[0]
        self.args = args[1:]
        self.process = mltprocess.Process(target=auto_buy
                                        , name=self.name
                                        , args=self.args
                                        , daemon=daemon)
        log.debug('created a process: Process=' + self.name)

    def is_alive(self):
        return self.process.is_alive()

    def is_dead(self):
        return self.flag_dead

    def is_started(self):
        return self.flag_started

    def start(self):
        if not self.process.is_alive():
            log.debug('the process starting: Process=' + self.name)
            self.process.start()
            self.flag_started = True
    
    def kill(self):
        if self.process.is_alive():
            log.debug('the process stopping: Process=' + self.name)
            self.process.kill()
            self.process.join()
            self.flag_dead = True

if __name__ == '__main__':
    # initializing a program
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', type=int, help='set the level of logging', default=2)
    opt = parser.parse_args()
    log.setLevel(opt.debug * 10) # 1:debug | 2:info | 3:warning | 4:error | 5:critical
    if opt.debug == 1:
        print(opt, '\n')
    log.info('initialized the program')
    
    # user interfaces
    while True:
        # input operation
        print('\nSyntax: {item1},{item2}... <blank> {target} [exit:Exit program]')
        operation = input('> input the operation: ')

        # processing exit operation
        if operation == 'exit':
            log.info('Program will exit')
            break

        # processing operation
        list_operation = operation.split(' ')
        if isinstance(list_operation, list) and len(list_operation) >= 2:
            items = list_operation[0].split(',')
            target = list_operation[1]
            log.debug('operation: items=[' + list_operation[0] + '] | target=' + list_operation[1])
        else:
            log.error('invalid syntax for operation: Operation=' + operation)
            continue
        
        # check all symbol in item operation
        # check valid item with registered items as anno1800()
        if not items[0] == '*':
            for item in items:
                if not anno1800.is_item(None, item):
                    log.error('invalid the item defined as operation: item=' + item)
                    continue

        # check valid store with registered stores as anno1800()
        # TO-DO: must be separated a store and a target
        if not anno1800.is_store(None, target):
            log.error('invalid the store defined as operation: store=' + target)
            continue
        
        # create a process and register a hotkey
        process = multiprocess(['auto_buy', items, target])
        keyboard.add_hotkey('f1', lambda: process.start())
        keyboard.add_hotkey('f9', lambda: process.kill())
        log.info('Press the key: [F1]:Start | [F9]:Stop')
        while True:
            try:
                if process.is_dead() and process.is_started():
                    log.info('Work done')
                    break
            except:
                log.warning('Work done with exception')
                break