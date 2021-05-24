import socket

def ipcheck():
	return socket.gethostbyname(socket.getfqdn())

print(ipcheck())

print("Host Name ",socket.gethostname())
 
print("IP Address(Internal) : ",socket.gethostbyname(socket.gethostname()))
 
print("IP Address(External) : ",socket.gethostbyname(socket.getfqdn()))