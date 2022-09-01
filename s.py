from socket import socket
from threading import Thread

s=socket()
s.bind(('',60002))
s.listen()
clients=[]
pkg_count=0

def boardcast(msg):
    for client in clients:
        client.send(msg)

def handle_a_client(c,addr):
    global pkg_count
    print('Handling',addr)
    while 1:
        try:
            msg=c.recv(1024)
            pkg_count+=1
            print(pkg_count,msg.decode())
            boardcast(msg)
        except:
            clients.remove(c)
            c.close()
            print(addr,'disconnected from server!')
            break

while 1:
    c,addr=s.accept()
    print(addr,'connected to server!')
    # c.close()
    Thread(target=handle_a_client,args=(c,addr,)).start()
    clients.append(c)