from tkinter import *
from functools import partial
import time
import mouse
import socket
import re
from pynput import keyboard
import threading


def connect(ip, port):
	created_window = False
	made = False

	root = Tk()

	root.attributes('-alpha', 0.01)
	root.attributes('-fullscreen', True)
	root.config(cursor='none')

	HOST = ip
	PORT = int(port)

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
					if event.x > (screen_dimensions[0] - 5) and not created_window and not made:
						created_window = True
						made = True
						root.update()
						mouse.move(100, mouse.get_position()[1])
					elif event.x > (screen_dimensions[0] - 5) and made and not created_window:
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
		
def connect_thread(ip, port):
	connect_thread = threading.Thread(target=connect, args=(ip.get(), port.get()))
	connect_thread.start()

tk_window = Tk()
tk_window.geometry('200x150')
tk_window.title('Sinkron')

ip_label = Label(tk_window, text="IP Adress").grid(row=0, column=0)
ip = StringVar()
ip_entry = Entry(tk_window, textvariable=ip).grid(row=0, column=1)

port_label = Label(tk_window, text="Port").grid(row=1, column=0)
port = StringVar()
port_entry = Entry(tk_window, textvariable=port).grid(row=1, column=1)

connect_thread = partial(connect_thread, ip, port)

connect_button = Button(tk_window, text="Connect", command=connect_thread).grid(row=4, column=0)

tk_window.mainloop()

# -
