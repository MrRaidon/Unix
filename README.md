Unix
Код для просто эхо-сервера:

Сервер:
```
import socket


add = ('', 9090)

sock = socket.socket()

sock.bind(add)
print('Сервер запущен', add)

sock.listen()
print('Прослушивания порта', add[1])

conn, addr = sock.accept()
print('Подключение клиента', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f'Прием данных {data.decode()}', addr)
    conn.send(data)

conn.close()
print('Отключение клиента', addr)

sock.listen()
print('Прослушивания порта', add[1])

conn, addr = sock.accept()
print('Подключение клиента', addr)

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f'Прием данных {data.decode()}', addr)
    conn.send(data)

sock.close()
print('Остановка сервера', add)

```

Клиент:
```
import socket

login="glushchenko"
password="123"

print("Чтобы продолжить введите логин и пароль через запятую (glushchenko,123)")
login, password = input().split(',')
if login=="glushchenko" and password=="123":
    add = ('', 9090)

    print('ведите хост и порт через запятую')
    name, port = input().split(',')
    if name == "0" and port == "0":
        name, port = '', 9090
    sock = socket.socket()

    sock.connect((name, int(port)))
    print('Соединение с сервером', (name, int(port)))

    while True:
        msg = input()
        if msg == 'exit':
            break
        sock.send(msg.encode())
        print(f'Отправка данных {msg}', (name, int(port)))
        data = sock.recv(1024)
        data_dec = data.decode()

    sock.close()
    print ('Разрыв соединения с сервером')
else:
    print("Неверный логин или пароль")

```
