import pickle
import socket


class FileCrypter:
    def __init__(self, key: int):
        self.key = key

    def encryption(self, message: str) -> str:
        return "".join([chr(ord(message[i]) ^ self.key) for i in range(len(message))])


class DiffieHellman:

    def __init__(self, a: int, p: int, g: int):
        self._a = a
        self._p = p
        self._g = g

    @property
    def mix(self):
        return self._g ** self._a % self._p

    def generate(self, mixed_key):
        return mixed_key ** self._a % self._p


HOST = '127.0.0.1'
PORT = 2022


def main():
    print('Введите хост и порт через запятую (0,0 для стандартного заполнения) ')
    host, port = input().split(',')
    if host == "0" and port == "0":
        HOST = '127.0.0.1'
        PORT = 2022
    sock = socket.socket()
    sock.connect((HOST, PORT))

    p_for_clip = 54
    g_for_clip = 53
    a_for_clip = 63

    diffie_hellman = DiffieHellman(a=a_for_clip, p=p_for_clip, g=g_for_clip)
    client_mixed_key = diffie_hellman.mix
    private_key = diffie_hellman.generate(client_mixed_key)
    print("Mix key", client_mixed_key)
    print("Privat key",private_key)

    sock.send(pickle.dumps((p_for_clip, g_for_clip, client_mixed_key)))
    sock.close()

    sock = socket.socket()
    sock.connect((HOST, PORT))
    crypter = FileCrypter(private_key)
    result = crypter.encryption("Sending is comlete")
    print("Crypted text: ", result)
    sock.send(pickle.dumps(result))

    result = crypter.encryption(result)
    print("Encrypted text: ", result)

    sock.close()


if __name__ == "__main__":
    main()
