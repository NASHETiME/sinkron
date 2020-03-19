from tkinter import *
import time
import mouse
import socket
import re
from pynput import keyboard

created_window = False
made = False

root = Tk()

root.attributes('-alpha', 0.01)
root.attributes('-fullscreen', True)
root.config(cursor='none')

HOST = '192.168.137.35'
PORT = 6546



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))

	

	events = []
	mouse.hook(events.append)

	def on_press(key):
		if created_window:
			try:
				s.sendall(('kbpa:' + key.char).encode('utf-8'))
			except AttributeError:
				s.sendall(('kbps:' + str(key)).encode('utf-8'))

	def on_release(key):
		if created_window:
			try:
				s.sendall(('kbra:' + key.char).encode('utf-8'))
			except AttributeError:
				s.sendall(('kbrs:' + str(key)).encode('utf-8'))
		if key == keyboard.Key.esc:
			# Stop listener
			return False

	# ...or, in a non-blocking fashion:
	listener = keyboard.Listener(
		on_press=on_press,
		on_release=on_release)
	listener.start()

	while 1:
		mouse._listener.queue.join()
		for event in events:

			# etype = str(type(event))[re.search('\'.+\'', str(type(event))).span()[0]:re.search('\'.+\'', str(type(event))).span()[1]].split('.')[-1][:-1]
			print(event)

			if created_window:
				root.update()
				s.sendall((str(event)).encode('utf-8'))

			try:
				if event.x > 1022 and not created_window and not made:
					created_window = True
					made = True
					root.update()
					mouse.move(100, mouse.get_position()[1])
				elif event.x > 1022 and made and not created_window:
					root = Tk()

					root.attributes('-alpha', 0.01)
					root.attributes('-fullscreen', True)
					root.config(cursor='none')
					created_window = True
					root.update()
					mouse.move(100, mouse.get_position()[1])
				elif event.x < 1 and created_window:
					created_window = False
					root.destroy()
					mouse.move(1300, mouse.get_position()[1])
			except:
				pass

		del events[:]
	
print('Received', repr(data))