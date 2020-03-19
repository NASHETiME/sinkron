import socket
import mouse
import time
import re

HOST = '192.168.137.1'
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	conn, addr = s.accept()
	with conn:
		print('Connected by: ', addr)
		while True:
			data = conn.recv(1024)
			if not data:
				break
			point = data.decode('utf-8')
			
			try:
				x = re.search('x=\d+', point).span()
				y = re.search('y=\d+', point).span()
				t = re.search('time=[\d.]+', point).span()

				x = int(point[x[0]:x[1]].split('=')[1])
				y = int(point[y[0]:y[1]].split('=')[1])
				t = float(point[t[0]:t[1]].split('=')[1])

				print(x, y, time.time() - t)
				mouse.move(x, y, duration=0)
			except:
				if point.split('(')[0] == 'ButtonEvent':
					e = re.search('event_type=\'.+\'', point).span()
					b = re.search('button=\'.+\'', point).span()
					t = re.search('time=[\d.]+', point).span()

					event_type = point[e[0]:e[1]].split('=')[1].split(',')[0][1:-1]
					button = point[b[0]+1:b[1]-1].split('=')[1][1:]
					t = float(point[t[0]:t[1]].split('=')[1])

					if button != '?':
						if event_type == 'up': mouse.release(button)
						if event_type == 'down': mouse.press(button)

			# mouse.move(x, y, duration=0.1)
			conn.sendall(data)