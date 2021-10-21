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
