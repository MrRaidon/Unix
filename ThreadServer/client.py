import socket
import json
import hostANDport

sock = socket.socket()

print('ведите хост и порт через запятую')
host, port = input().split(',')
if host == "0" and port == "0":
    host = hostANDport.HOST
    port = hostANDport.PORT

print("Чтобы продолжить введите логин и пароль через запятую (glushchenko,123)")
login, password = input().split(',')
info = {'login': login, 'password': password}
sock.connect((host, int(port)))
sock.send(bytes(json.dumps(info).encode()))
status = sock.recv(1024)
if status.decode('UTF-8') == 'CONTINUE':
    while True:
        sock.send(bytes(input().encode()))
        data = sock.recv(1024)
        print(str(data.decode()))
        if data.decode('UTF-8') == 'CLOSETHREAD':
            print("Поток закрыт")
            break
sock.close()
