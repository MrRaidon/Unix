import mimetypes
import os
import socket
import argparse


class BrowserRequest():

    def __init__(self, data: bytes):
        lines = [d.strip() for d in data.decode('utf8','replace').split("\n") if d.strip()]

        self.method, self.path, self.http_version = lines.pop(0).split(" ")
        self.info = {k: v for k, v in (l.split(': ') for l in lines)}

    def __repr__(self) -> str:
        return "<BrowserRequest {method} {path} {http_version}>".format(
            method=self.method, path=self.path, http_version=self.http_version)

    def __getattr__(self, name: str):
        try:
            return self.info["-".join([n.capitalize() for n in name.split('_')])]
        except IndexError:
            raise AttributeError(name)


class ServerSocket():

    def __init__(self, host='', port=80, buffer_size=1024, max_queued_connections=5):
        self._connection = None
        self._socket = None
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self.max_queued_connections = max_queued_connections

    def __repr__(self) -> str:
        status = 'closed' if self._socket is None else 'open'
        return "<{status} ServerSocket {host}:{port}>".format(
            status=status, host=self.host, port=self.port)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        assert self._socket is None, "ServerSocket is already open"
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self._socket.bind((self.host, self.port))
        except:
            self.close()
            raise
        else:
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def close(self):
        assert self._socket is not None, "ServerSocker is already closed"
        if self._connection:
            self._connection.close()
            self._connection = None
        self._socket.close()
        self._socket = None

    def listen(self) -> BrowserRequest:
        assert self._socket is not None, "ServerSocker must be open to listen data"
        self._socket.listen(self.max_queued_connections)
        self._connection, _ = self._socket.accept()
        data = self._connection.recv(self.buffer_size)
        return BrowserRequest(data)

    def respond(self, data: bytes):
        assert self._socket is not None, "ServerSocker must be open to respond"
        self._connection.send(data)
        self._connection.close()


class SimpleServer():



    def __init__(self, port=80, homedir=os.path.curdir, page404=None):
        self.socket = ServerSocket(port=port)
        self.homedir = os.path.abspath(homedir)

    log_format = "{method} {path} {user_agent}"

    def log(self, msg: str):
        print(msg)

    def serve(self):
        self.socket.open()
        self.log('Opening socket connection {}:{} in {}'.format(
            self.socket.host, self.socket.port, self.homedir))
        while True:
            self.serve_request()

    def stop(self):
        self.socket.close()

    def serve_request(self):
        request = self.socket.listen()
        path = request.path
        try:
            body, status_code = self.load_file(path)
        except IsADirectoryError:
            path = os.path.join(path, 'index.html')
            body, status_code = self.load_file(path)

        header = self.get_header(status_code, path)
        self.socket.respond((header + body).encode())

        self.log(self.log_format.format(method=request.method,
                                        path=request.path,
                                        user_agent=request.user_agent))
    def get_header(self, status_code: int, path: str):
        _, file_ext = os.path.splitext(path)
        return "\n".join([
            "HTTP/1.1",
            "Content-Type: {}".format(mimetypes.types_map.get(file_ext, 'application/octet-stream')),
            "Server: Hello WebWorld"
            "\n\n"
        ])

    def load_file(self, path):        
        try:
            with open(os.path.join(self.homedir, path.lstrip('/'))) as f:
                return f.read(), 200
        except FileNotFoundError:
            return self.response_404, 404



parser = argparse.ArgumentParser()
parser.add_argument('port', type=int, help='port to run the server on')
args = parser.parse_args()
server = SimpleServer(args.port)
try:
    server.serve()
except:
    os._exit(0)
finally:
    server.stop()
