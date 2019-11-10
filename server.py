# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
from thread import *
from diffiehellman import diffiehellman
from pydes import des

dh = diffiehellman(7919, 18446744073709551615)
d = des()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# checks whether sufficient arguments have been provided 
if len(sys.argv) != 3: 
	print("Correct usage: script, IP address, port number")
	exit() 

# takes the first argument from command prompt as IP address 
IP_address = str(sys.argv[1]) 

# takes second argument from command prompt as port number 
Port = int(sys.argv[2]) 

server.bind((IP_address, Port)) 
server.listen(100) 

def listenThread(conn, addr): 
	# sends a message to the client whose user object is conn 
	sendMessage("/key "+str(dh.generate_partial_key()), conn)
	flag = 0
	while(not flag):
			try: 
				message = conn.recv(2048) 
				if message[:4] == "/key": 
					dh.generate_full_key(int(message[5:]))
					flag = 1
				else: 
					pass

			except: 
				continue

def sendMessage(message, connection): 
	try: 
		connection.send(message) 
	except: 
		remove(connection) 

def remove(connection): 
	connection.close() 

conn, addr = server.accept() 

# prints the address of the user that just connected 
print(addr[0] + " connected")

# creates and individual thread for every user 
# that connects 
start_new_thread(listenThread,(conn,addr))

while(True):
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, conn] 
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
	for socks in read_sockets: 
		if socks == conn: 
			message = socks.recv(2048) 
			message = d.decrypt(dh.get_full_key(), message, True)
			print("client: "+message)
		else: 
			message = socks.readline() 
			message_enc = d.encrypt(dh.get_full_key(), message, True)
			sendMessage(message_enc,conn) 
			sys.stdout.write("You: ") 
			sys.stdout.write(message) 
			sys.stdout.flush() 

conn.close() 
server.close() 
