Unix
Код для просто эхо-сервера:

Сервер:
```
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

```

Клиент:
```

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


```

Логи:
```
INFO:echo-server: Client glushchenko login on 2021-11-16 17:38:24.435762
INFO:echo-server: Input asd on 2021-11-16 17:38:28.147401
INFO:echo-server: Input qwe on 2021-11-16 17:38:31.945025
INFO:echo-server: Client glushchenko login on 2021-11-16 17:38:43.969088
INFO:echo-server: Input asd on 2021-11-16 17:38:45.113478
INFO:echo-server: Input qwe on 2021-11-16 17:38:46.172442
INFO:echo-server: Input None on 2021-11-16 17:39:18.202122
INFO:echo-server: Input None on 2021-11-16 17:39:20.766284
INFO:echo-server: Client glushchenko login on 2021-11-16 17:41:37.914219
INFO:echo-server: Input CLOSE on 2021-11-16 17:42:20.322858
INFO:echo-server: Input None on 2021-11-16 17:42:20.324518
INFO:echo-server: Client glushchenko login on 2021-11-16 17:45:25.172971
INFO:echo-server: Input None on 2021-11-16 17:46:51.136641
INFO:echo-server: Client glushchenko login on 2021-11-16 17:47:04.818354
INFO:echo-server: Input qwe on 2021-11-16 17:47:06.504094
INFO:echo-server: Client glushchenko login on 2021-11-16 17:47:36.625211
INFO:echo-server: Input qwe on 2021-11-16 17:47:37.956058
INFO:echo-server: Input exit on 2021-11-16 17:52:59.983020
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:55:07.778248
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:55:44.035025
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:56:23.576031
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:58:03.303058
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:58:36.025554
INFO:echo-server: Input asd on 2021-11-16 17:58:41.607297
INFO:echo-server: Input qweqe on 2021-11-16 17:58:43.588425
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 17:58:52.115468
INFO:echo-server: Input asdasd on 2021-11-16 17:58:56.417655
INFO:echo-server: Input qwe on 2021-11-16 17:58:57.302818
INFO:echo-server: Input exit on 2021-11-16 17:59:08.734674
INFO:echo-server: Input exit on 2021-11-16 17:59:11.993097
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:07:50.019480
INFO:echo-server: Input qwe on 2021-11-16 18:07:52.417848
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:11:13.202533
INFO:echo-server: Input wqe on 2021-11-16 18:11:17.481139
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:12:21.698542
INFO:echo-server: Input asd on 2021-11-16 18:12:22.419845
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:12:47.951972
INFO:echo-server: Input qwe on 2021-11-16 18:12:48.887157
INFO:echo-server: Input exit on 2021-11-16 18:14:28.601012
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:14:53.150197
INFO:echo-server: Input qwe on 2021-11-16 18:14:54.260067
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:15:13.293064
INFO:echo-server: Input asd on 2021-11-16 18:15:14.574288
INFO:echo-server: Input None on 2021-11-16 18:17:09.324286
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:17:14.378505
INFO:echo-server: Input 123 on 2021-11-16 18:17:15.030215
INFO:echo-server: Input None on 2021-11-16 18:19:51.462995
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:20:25.809311
INFO:echo-server: Input awd on 2021-11-16 18:20:27.078335
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:22:34.064903
INFO:echo-server: Input 123 on 2021-11-16 18:22:36.232119
INFO:echo-server: Client ['glushchenko', 'nikita'] login on 2021-11-16 18:22:51.220963
INFO:echo-server: Input wer on 2021-11-16 18:22:52.245919
INFO:echo-server: Input exit on 2021-11-16 18:23:00.590804
INFO:echo-server: Input exit on 2021-11-16 18:23:04.538542

```
