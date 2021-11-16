import json
import socket
import logging
import hashlib
from datetime import datetime
import hostANDport
import threading
flag=1
LOGIN = ['glushchenko','nikita']
PASSWORD = ['123','456']
logging.basicConfig(filename='serverThreads.log')
logger = logging.getLogger('echo-server')
logger.setLevel(logging.DEBUG)

sock = socket.socket()
sock.bind((hostANDport.HOST, hostANDport.PORT))
sock.listen(5)

def clients(conn, addr):
    info = json.loads(conn.recv(1024).decode('UTF-8'))
    for i in range(len(LOGIN)):
        if info['login'] == LOGIN[i] and info['password'] == PASSWORD[i]:
            logger.info(f' Client {LOGIN} login on {datetime.now()}')
            conn.send(bytes('CONTINUE'.encode()))
            print(f" Client {info['login']} connected")
            flag=0;
    if flag == 1:
            print("Wrong login or password")
            conn.close()
            sock.close()
            exit(0)

    while True:
        data = conn.recv(1024)
        text = data.decode('UTF-8') if data else None
        logger.info(f' Input {text} on {datetime.now()}')
        if text == 'exit' or not data:
            conn.send('CLOSETHREAD'.encode())
            conn.close()
            break
        else:
            print(f'Произошел прием данных на сервере {data.decode()} от {info["login"]}')
            conn.send(bytes(f'Произошел прием данных на сервере {data.decode()}'.encode()))


while True:
    conn, addr = sock.accept()
    print('New thread accepted')
    t = threading.Thread(target=clients, args=[conn, addr])
    t.start()
    print('New thread created')

sock.close()
