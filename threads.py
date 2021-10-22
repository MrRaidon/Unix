import threading


class T(threading.Thread):
    def __init__(self, n):
        threading.Thread.__init__(self, name="t" + n)
        self.n = n


def run(self):
    print("Процесс", self.n)


p1 = T("1")
p2 = T("2")
p1.start()
p2.start()
