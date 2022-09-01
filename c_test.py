from socket import socket
s=socket()
s.connect(('localhost',60002))
s.close()