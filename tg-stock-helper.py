# coding=utf-8
# скрипт для дефера
# раз в 2 часа ходит в пещеру, в нужную пару часов встаёт в деф

import tgl
import re
import time
# from threading import Thread
# from datetime import datetime
# from random import randint

TARGET_PEER_NAME = 'Chat_Wars'
LOG_PEER_NAME = 'Comcenter'
TRADEBOT_PEER_NAME = 'ChatWarsTradeBot'

our_id = 0
peers = []
target_peer = None
log_peer = None
trade_peer = None
# slots = [1, 1]
# need_stay_to_def = True
# log_needed = True
to_trade = None


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
        global peers, target_peer, log_peer, trade_peer, TARGET_PEER_NAME, LOG_PEER_NAME
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
            if dialog["peer"].name == TRADEBOT_PEER_NAME:
                print 'trade peer accepted'
                trade_peer = dialog["peer"]

def on_msg_receive(msg):
    global forming, trade_peer, to_trade
    if msg.out:
        return

    peer = msg.dest
    if msg.dest.id == our_id: # direct message
        peer = msg.src
        peer.mark_read()
    if msg.text is not None \
        and peer.name == TRADEBOT_PEER_NAME \
        and trade_peer \
        :
            if r'Твой склад с материалами' in msg.text.encode('utf8') and not to_trade:
                to_trade = list()
                # parse stock
                for line in msg.text.encode('utf8').split('\n'):
                    print line
                    m = re.match('(/add_\d+)\D+(\d+)', line)
                    if m:
                        to_trade.append(m.group(1) + ' ' + m.group(2))
                        print to_trade
                print len(to_trade)
                if len(to_trade):
                    trade_peer.send_msg(to_trade.pop())
                return
            if r'Твой склад с материалами' in msg.text.encode('utf8') and to_trade and len(to_trade):
                trade_peer.send_msg(to_trade.pop())
                return

def on_loop():
    pass
            
            
tgl.set_on_our_id(on_our_id)
tgl.set_on_msg_receive(on_msg_receive)
tgl.get_dialog_list(dialog_list_cb)
tgl.set_on_loop(on_loop)