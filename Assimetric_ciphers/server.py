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
PORT = 2020


def main():
    sock = socket.socket()
    sock.bind((HOST, PORT))
    sock.listen(1)

    crypter = None
    while True:
        conn, addr = sock.accept()

        text = conn.recv(4096)
        data = pickle.loads(text)

        if type(data) == tuple:
            p_for_clip_Serv, g_for_clip_Serv, a_for_clip_Serv = data

            diffie_hellman = DiffieHellman(a=a_for_clip_Serv, p=p_for_clip_Serv, g=g_for_clip_Serv)
            server_mixed_key = diffie_hellman.mix
            private_key = diffie_hellman.generate(server_mixed_key)
            crypter = FileCrypter(private_key)
            print("Mix key from server", server_mixed_key)
            print("Privates key", private_key)

        elif type(data) == str:
            result = crypter.encryption(data)
            print("Encrypted key", result)

        else:
            raise ValueError(f"Был принят неверный тип: {type(data)}")


if __name__ == "__main__":
    main()
