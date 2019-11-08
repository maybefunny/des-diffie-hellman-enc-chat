# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from diffiehellman import diffiehellman
from pydes import des

dh = diffiehellman(7919, 104729)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
server.connect((IP_address, Port)) 

# maintains a list of possible input streams 
sockets_list = [sys.stdin, server] 
read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 

server.send("/key "+str(dh.generate_partial_key()))
flag = 0
while(not flag):
	try: 
		for socks in read_sockets: 
			if socks == server: 
				message = socks.recv(2048) 
				if message[:4] == "/key": 
					flag = 1
				else:
					pass
			else: 
				pass

	except: 
		continue

while True: 
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048) 
			print("server: "+message)
		else: 
			message = sys.stdin.readline() 
			server.send(message) 
			sys.stdout.write("You: ") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 
