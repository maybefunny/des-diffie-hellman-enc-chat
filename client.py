# Python program to implement client side of chat room. 
import socket 
import select 
import sys 
from diffiehellman import diffiehellman
from pydes import des

dh = diffiehellman(7919, 18446744073709551615)
d = des()

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
					dh.generate_full_key(int(message[5:]))
					flag = 1
				else:
					pass
			else: 
				pass

	except: 
		continue

print(dh.get_full_key())

while True: 
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, server] 
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
	for socks in read_sockets: 
		if socks == server: 
			message = socks.recv(2048) 
			message = d.decrypt(dh.get_full_key(), message, True)
			print("server: "+message)
		else: 
			message = sys.stdin.readline() 
			message_enc = d.encrypt(dh.get_full_key(), message, True)
			server.send(message_enc) 
			sys.stdout.write("You: ") 
			sys.stdout.write(message) 
			sys.stdout.flush() 
server.close() 
