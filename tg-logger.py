# coding=utf-8

import tgl
from logger import Logger


our_id = 0
i = 0
peers = []
log = Logger()


def on_our_id(id):
    global our_id
    our_id = id
    return "Set ID: " + str(our_id)

def contact_list_cb(success, peer_list):
	if success:
		global peers
		peers = peer_list
		for p in peers:
			print(p.name)

def dialog_list_cb(success, dialog_list):
	if success:
		global peers
		for dialog in dialog_list:
			peers.append(dialog["peer"].name)
			print(dialog["peer"].name)

def msg_cb(success, msg):
    print("sent")

def on_msg_receive(msg):
    if msg.out:
        return

    peer = msg.dest    
    if peer:    	
    	if msg.text is not None and peer.name == 'Comcenter':
    		log.log(msg.text)
    		peer.send_msg('🇻🇦')
        	

def on_loop():
    pass

# Set callbacks
#tgl.set_on_binlog_replay_end(on_binlog_replay_end)
#tgl.set_on_get_difference_end(on_get_difference_end)
tgl.set_on_our_id(on_our_id)
tgl.set_on_msg_receive(on_msg_receive)
#tgl.set_on_secret_chat_update(on_secret_chat_update)
#tgl.set_on_user_update(on_user_update)
#tgl.set_on_chat_update(on_chat_update)
tgl.set_on_loop(on_loop)

tgl.get_contact_list(contact_list_cb)
tgl.get_dialog_list(dialog_list_cb)