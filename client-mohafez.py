import socket
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('127.0.0.1',9999))
got=client.recv(4096)
print(got.decode())
val='hey you server'
client.send(val.encode())
#client.send(b'Salam')
