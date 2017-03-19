# coding=utf-8
# скрипт для дефера
# раз в 2 часа ходит в пещеру, в нужную пару часов встаёт в деф

import tgl
import os
import time
from threading import Thread
from datetime import datetime
from random import randint

TARGET_PEER_NAME = 'Chat_Wars'
LOG_PEER_NAME = 'Comcenter'

our_id = 0
peers = []
target_peer = None
log_peer = None
slots = [1, 1]
need_stay_to_def = True
log_needed = True


def thread_heartbeat():
    while True:
        print(time.ctime())
        time.sleep(10)
    
def on_our_id(id):
    global our_id
    our_id = id
    return "Set ID: " + str(our_id)

def dialog_list_cb(success, dialog_list):
    if success:
        global peers, target_peer, log_peer, TARGET_PEER_NAME, LOG_PEER_NAME
        # global 
        for dialog in dialog_list:
            peers.append(dialog["peer"].name)
            print dialog["peer"].name
            if dialog["peer"].name == TARGET_PEER_NAME:
                print 'peer accepted'
                target_peer = dialog["peer"]
            if dialog["peer"].name == LOG_PEER_NAME:
                print 'log peer accepted'
                log_peer = dialog["peer"]

def on_msg_receive(msg):
    global log_peer
    if msg.out:
        return

    peer = msg.dest
    if msg.dest.id == our_id: # direct message
        peer = msg.src
        peer.mark_read()
    if msg.text is not None \
        and peer.name == TARGET_PEER_NAME \
        :
            time.sleep(1)
            if 'Грабить корованы — дело опасное. Могут заметить и' in msg.text.encode('utf8'):
                peer.send_msg('🕸Пещера')
            if 'Храбрый защитник! Где будем держать оборону?' in msg.text.encode('utf8'):
                peer.send_msg('🇮🇲')
                log_peer.send_msg('defending castle')
            if '/go' in msg.text.encode('utf8'):
                peer.send_msg('/go')

    if msg.text is not None \
        and peer.name == 'Telegram' \
        :
        with open('/home/ubuntu/work/tgscripts/profiles/codes', 'w') as f:
            f.write(time.ctime())
            f.write(os.linesep)
            f.write(msg.text.encode('utf8'))

def on_loop():
    global target_peer, log_needed, log_peer, need_stay_to_def
#    print 'on_loop ', slots, datetime.now().hour
#    print datetime.now().minute, log_needed, log_peer
    if datetime.now().hour % 4 == 1 and datetime.now().minute == slots[0] and slots[0] and target_peer:
        slots[1] = randint(10,30)
        slots[0] = 0
        need_stay_to_def = True
        target_peer.send_msg('🗺 Квесты')
        log_peer.send_msg(time.ctime())
    if datetime.now().hour % 4 == 3 and datetime.now().minute == slots[1] and slots[1] and target_peer:
        slots[1] = 0
        slots[0] = randint(10,30)
        target_peer.send_msg('🗺 Квесты')
    if datetime.now().hour % 4 == 3 and datetime.now().minute == 50 and need_stay_to_def and target_peer:
        need_stay_to_def = False
        target_peer.send_msg('🛡 Защита')
        log_peer.send_msg('going to def')
#    if datetime.now().minute % 4 == 1 and log_needed and log_peer:
#        log_needed = False
#        log_peer.send_msg(time.ctime())
#    if datetime.now().minute % 4 == 0 and not log_needed:
#        log_needed = True

tgl.set_on_our_id(on_our_id)
tgl.set_on_msg_receive(on_msg_receive)
tgl.get_dialog_list(dialog_list_cb)
tgl.set_on_loop(on_loop)

# запускаем поток для выстрела сообщений
# t = Thread(target=thread_heartbeat)
# t.start()
