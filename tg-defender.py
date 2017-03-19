# coding=utf-8
# скрипт для дефера

import tgl
our_id = 0
i = 0
peers = []

binlog_done = False;

def on_binlog_replay_end():
    global binlog_done
    binlog_done = True;

def on_get_difference_end():
    pass

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
    global i
    if msg.out:
        return

    peer = None
    if msg.dest.id == our_id: # direct message
        print("to me")
        peer = msg.src
        peer.mark_read()
    if peer:
    	print(peer.name)
    	if msg.text is not None and msg.text.startswith("PING"):
        	peer.send_msg("PONG")
    else:
    	print("None")    
    i += 1
    print(i)


def on_secret_chat_update(peer, types):
    return "on_secret_chat_update"

def on_user_update(peer, what_changed):
    pass

def on_chat_update(peer, what_changed):
    pass

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