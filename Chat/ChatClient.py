import socket
import threading
import random
import os
import PORT

firstdata='000'
host=socket.gethostbyname(socket.gethostname())
port=PORT.port
print('Чтобы остановить сервер- введите stopServer, - exit, чтобы удалить аккаунт и выйти - DelClient')

def ReceiveData(sock):
    global firstdata
    while True:
        try:
            data,addr = sock.recvfrom(1024)
            firstdata = data.decode('utf-8')
            if firstdata == 'exit':
                print(firstdata)
            else:
                print(data)
        except:
            pass


port = random.randint(6000,10000)
server = (socket.gethostbyname(socket.gethostname()),PORT.port)
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

s.bind((host,port))

while True:
    name = input('Введите свое имя ')
    if name == '':
        print('Вы не ввели имя, это обязательно')
    else:
        break

s.sendto(name.encode('utf-8'),server)
threading.Thread(target=ReceiveData,args=(s,)).start()
while True:
    if firstdata == 'exit':
        break
    data = input()
    if (data == 'DelClient' or data == 'stopServer'):
        break
    elif data=='':
        continue
    elif data=='exit':
        break
    data = '['+name+']' + '->'+ data
    s.sendto(data.encode('utf-8'),server)
s.sendto(data.encode('utf-8'),server)
s.close()
os._exit(1)
