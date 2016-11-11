class URL(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __repr__(self):
        return "http://" + self.host + ":" + str(self.port)

class Config:
    def __init__(self):
        self.projetox9 = URL("0.0.0.0", 5000)
        self.FakeSiga  = URL("0.0.0.0", 3000)
        self.mongodb   = URL("0.0.0.0", 0000)
