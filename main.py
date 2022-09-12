
from operator import itemgetter
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

class event:
    def __init__(self, flag=False):
        self.flag = flag

    def set(self, flag):
        self.flag = flag

    def get(self):
        return self.flag
    
    def toggle(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True


def auto_buy(items, type_store, skip_trade_button=True):
    from anno1800.anno1800 import anno1800
    from anno1800.detect import detect
    work_done = event()
    log.debug('items=[' + ','.join(items) + '] | type_store=' + type_store)

    anno1800 = anno1800()

    list_items = anno1800.format_items(items, type_store)

    det_items = detect(list_items
                    , anno1800.stores[type_store].region['list_items'], threshold_conf=0.90, delay=0.2)
    det_store = detect(anno1800.stores[type_store].image
                    , anno1800.stores[type_store].region['id'])
    det_state_no_inventory = detect(anno1800.stores[type_store].image_states['no_inventory']
                                , anno1800.stores[type_store].region['no_inventory'])
    det_state_out_of_stock = detect(anno1800.stores[type_store].image_states['out_of_stock']
                                , anno1800.stores[type_store].region['out_of_stock'])                
    det_ship_trade_button = detect(anno1800.facilities['ship'].image_states['trade']
                                , anno1800.facilities['ship'].region['trade'])

    while(True):
        if work_done.get():
            break
        if det_ship_trade_button.find() or skip_trade_button:
            log.debug('detected the button of the ship trade')
            time.sleep(0.2)
            if not skip_trade_button:
                anno1800.windows.click_button('ship', 'trade')
            anno1800.windows.click_button(type_store, 'tab_trade_item')
            log.debug('trying to detect...') 
            while(True):
                if not det_state_no_inventory.find():
                    if not det_state_out_of_stock.find():
                        dets = det_items.get_coords()
                        if len(dets) > 0:
                            dets.sort(key=itemgetter(2, 1), reverse=True)
                            for det in dets:
                                log.debug(det)
                                anno1800.windows.click(det[1:], delay=0.0)
                                anno1800.windows.click_button(type_store, 'trade_done', delay=0.1)
                            dets = []
                        anno1800.windows.click_button(type_store, 'dice')
                    else:
                        log.info('detected out of stock')
                        anno1800.windows.click_button(type_store, 'exit')
                        work_done.set(True)
                        break
                else:
                    log.info('detected no inventory')
                    anno1800.windows.click_button(type_store, 'exit')
                    work_done.set(True)
                    break
        else:
            log.debug('waiting for the button of the ship trade...')
            time.sleep(1)
    log.debug('process done')
    return


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
        log.debug('created the process: Process=' + self.name)

    def is_alive_c(self):
        return self.process.is_alive()

    def is_dead(self):
        return self.flag_dead

    def is_started(self):
        return self.flag_started

    def start(self):
        if not self.process.is_alive():
            log.debug('starting the process: Process=' + self.name)
            self.process.start()
            self.flag_started = True

    def kill(self):
        if self.process.is_alive():
            log.debug('stopping the process: Process=' + self.name)
            self.process.kill()
            self.process.join()
            self.flag_dead = True


if __name__ == '__main__':
    # initializing a program
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='set the level of logging', default=False)
    opt = parser.parse_args()
    log.setLevel(10 if opt.debug else 20) # 10:debug | 20:info | 30:warning | 40:error | 50:critical
    if opt.debug == 1:
        print(opt, '\n')
    log.info('initialized the program')

    escape = event()
    # user interfaces
    while True:
        escape.set(False)
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
        
        while True:
            if escape.get():
                process.kill()
                log.info('Terminated the operation')
                break
            # create a process and register a hotkey
            process = multiprocess(['auto_buy', items, target])
            keyboard.add_hotkey('f1', lambda: process.start())
            keyboard.add_hotkey('f5', lambda: process.kill())
            keyboard.add_hotkey('f9', lambda: escape.set(True))
            log.info('Press the key: [F1]:Start | [F5]:Stop | [F9]:Exit')
            time.sleep(2)
            while True:
                try:
                    if escape.get():
                        break
                    if (process.is_alive_c() == False) and process.is_started():
                        try:
                            log.debug('try to kill the process: is_alive_c=' + process.is_alive_c() + " | is_started=" + process.is_started())
                            process.kill()
                        except:
                            log.warning('cannot terminate the process: is_alive_c=' + process.is_alive_c() + " | is_started=" + process.is_started())

                        log.info('Work done')
                        break
                except:
                    log.warning('Work done with exception')
                    break

            # t4_guard,t4_propeller equipments
            # t4_attack_abraheem,t4_attack_roo,t4_harbor_speed,t4_investor people