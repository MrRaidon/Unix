import socket
import threading
import queue
import os
import PORT


host=socket.gethostbyname(socket.gethostname())
port = PORT.port



def ResendingData(sock,info):
    while True:
        data,addr = sock.recvfrom(1024)
        info.put((data,addr))

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((host,port))
clients = set()   #последовательность клиентов
info = queue.Queue() #Очереди для потоков

print('Сервер запущен')

threading.Thread(target=ResendingData,args=(s,info)).start()

while True:
    while not info.empty():
        data,addr = info.get()
        if addr not in clients:
            clients.add(addr)
            continue
        clients.add(addr)
        data = data.decode('utf-8')
        if data.endswith('DelClient'):
            clients.remove(addr)
            continue
        if 'stopServer' in data:
            for every in clients:
                s.sendto('exit'.encode('utf-8'),every)
            s.close()
            os._exit(1)
        print(str(addr)+data)
        for every in clients:
            if every!=addr:
                s.sendto(data.encode('utf-8'),every)
s.close()

