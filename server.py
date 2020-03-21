import socket
import mouse
import time
import re
from pynput.mouse import Button, Controller
from pynput.keyboard import Key
import pynput.keyboard
import tkinter
import sys
from tkinter import *
from functools import partial
import threading

m = Controller()
k = pynput.keyboard.Controller()

def start_server(ip, port):
	HOST = ip
	PORT = int(port)

	currx = 0
	curry = 0

	#

	def set_display_properties():
		root = tkinter.Tk()
		root.attributes('-alpha', 0)
		root.attributes('-fullscreen', True)
		return (root.winfo_screenwidth(), root.winfo_screenheight())

	screen_dimensions = set_display_properties()

	#

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as main_socket:
		main_socket.bind((HOST, PORT))
		main_socket.listen()
		conn, addr = main_socket.accept()
		with conn:
			print('Connected by : ', addr)

			server_screen = conn.recv(1024).decode('utf-8')
			server_width = int(server_screen.split(':')[0])
			server_height = int(server_screen.split(':')[1])

			while True:
				data = conn.recv(1024)
				if not data: break

				point = data.decode('utf-8')

				try:
					if point.split(')')[1] == '':
						if point[:11] == 'ButtonEvent':
							button_event = eval('mouse.' + point)
							if button_event.event_type == 'up': m.release(button_event.button)
							elif button_event.event_type == 'down': m.press(button_event.button)

						else:
							mouse.play([eval('mouse.' + point)])

				except:
					if point[:2] == 'kb':
						if point[3] == 'a':
							if point[2] == 'r': k.release(point[5:])
							if point[2] == 'r': k.press(point[5:])
						elif point[3] == 's':
							if point[2] == 'r': k.release(eval(point[5:]))
							if point[2] == 'r': k.press(eval(point[5:]))

def start_server_thread(ip, port):
	main_server_thread = threading.Thread(target=start_server, args=(ip.get(), port.get()))
	main_server_thread.start()

tk_window = Tk()
tk_window.geometry('200x150')
tk_window.title('Sinkron')

ip_label = Label(tk_window, text="IP Adress").grid(row=0, column=0)
ip = StringVar()
ip_entry = Entry(tk_window, textvariable=ip).grid(row=0, column=1)

port_label = Label(tk_window, text="Port").grid(row=1, column=0)
port = StringVar()
port_entry = Entry(tk_window, textvariable=port).grid(row=1, column=1)

start_server_thread = partial(start_server_thread, ip, port)

start_server_button = Button(tk_window, text="Start Server", command=start_server_thread).grid(row=4, column=0)

tk_window.mainloop()

# -
