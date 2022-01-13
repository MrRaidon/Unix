import json
import socket
import logging
import os
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
'''
pwd - показывает название рабочей директории
ls - показывает содержимое текущей директории
mkdir - создает новую директорию
removeDir - удаляет директорию
remove - удаляет папку
rename - переименовывает папку
exitClient - отключение от сервера
serverStop - остановка сервера
create - создание файла
'''

dirname = os.path.join(os.getcwd(), 'savedir')

def process(req):
    req = req.split()
    if req[0] == 'pwd':
        return dirname
    elif req[0] == 'ls':
        return '; '.join(os.listdir(dirname))
    elif req[0] == 'mkdir':
        if not os.path.exists(os.path.join(dirname, req[1])):
            os.makedirs(os.path.join(dirname, req[1]))
            return os.path.join(dirname, req[1])
        else:
            return "Такая директория уже существует"
    elif(req[0] == 'removeDir'):
        os.rmdir(os.path.join(dirname, req[1]))
        return "Директория "+req[1]+" удалена"
    elif (req[0] == 'remove'):
        os.remove(os.path.join(dirname, req[1]))
        return "Папка " + req[1] + " удалена"
    elif (req[0] == 'rename'):
        os.rename(os.path.join(dirname, req[1]), os.path.join(dirname, req[2]))
        return "Папка " + req[1] + " переименована в "+req[2]
    elif (req[0] == 'create'):
        content = open(os.path.join(dirname, req[1]), 'a+')
        content.close()
        return "Файл " + req[1] + " создан "

    else:
        return 'Такой команды не существует'


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
        response = process(data.decode())

        text = data.decode('UTF-8') if data else None
        logger.info(f' Input {text} on {datetime.now()}')
        if text == 'exitClient' or not data:
            conn.send('CLOSETHREAD'.encode())
            conn.close()
            break
        elif text == 'serverStop' or not data:
            conn.send('CLOSETHREAD'.encode())
            conn.close()
            os._exit(1)
            break
        else:
            print(f'Произошел прием данных на сервере {conn.send(response.encode())} от {info["login"]}')


while True:
    conn, addr = sock.accept()
    print('New thread accepted')
    t = threading.Thread(target=clients, args=[conn, addr])
    t.start()
    print('New thread created')
sock.close()
