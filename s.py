from socket import socket
from threading import Thread
from json import load, dump

voxels=load(open('./s_checkpoint.json'))

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
    print('Sending checkpoint!')
    for z in voxels:
        c.send(('add+%s+%s;'%(z,voxels[z])).encode())
    print('Handling',addr)
    while 1:
        try:
            msg=c.recv(1024)
            cmds=msg.decode().split(';')
            # print(cmds)
            for cmd in cmds:
                cmd=cmd.split('+')
                if cmd[0]=='add':
                    voxels[cmd[1].replace('Vec3','')]=cmd[2]
                    dump(voxels,open('./s_checkpoint.json','w'))
                pkg_count+=1
                print(pkg_count,cmd)
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