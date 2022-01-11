import socket

login="glushchenko"
password="123"

print("Чтобы продолжить введите логин и пароль через запятую (glushchenko,123)")
login, password = input().split(',')
if login=="glushchenko" and password=="123":
    add = ('localhost', 9091)

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
