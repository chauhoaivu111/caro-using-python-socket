import threading
import socket



class Threading_socket():
    def __init__(self, gui):
        super().__init__()
        self.dataReceive = ""
        self.conn = None
        self.gui = gui
        self.name = ""

    def clientAction(self, inputIP):
        self.name = "client"
        print("client connecting ...............")
        # Configure server address
        HOST = inputIP  
        # Configure the port to use
        PORT = 8000            
        self.conn = socket.socket(
            # Socket configuration
            socket.AF_INET, socket.SOCK_STREAM) 
        self.conn.connect((HOST, PORT)) 
        self.gui.notification("connected successfully", str(HOST))
        # make a connection to the server
        t1 = threading.Thread(target=self.client)  
        # create client thread
        t1.start()

    def client(self):
        while True:
            # Read server return data
            self.dataReceive = self.conn.recv(
                1024).decode() 
            if(self.dataReceive != ""):
                friend = self.dataReceive.split("|")[0]
                action = self.dataReceive.split("|")[1]
                if(action == "hit" and friend == "server"):
                    #     print(self.dataReceive)
                    x = int(self.dataReceive.split("|")[2])
                    y = int(self.dataReceive.split("|")[3])
                    self.gui.ButtonHandle(x, y)
                if(action == "Undo" and friend == "server"):

                    self.gui.Undo(False)
            self.dataReceive = ""

    def serverAction(self):
        self.name = "server"
        HOST = socket.gethostbyname(socket.gethostname())  
        print("Get IP.........." + HOST)
        # Set up an address
        self.gui.notification("your IP", str(HOST))
        # Set listening port
        PORT = 8000  
        # configure connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # listen port 
        s.bind((HOST, PORT))  
        # set up 1 concurrent connection
        s.listen(1)  
        # accept connection and return parameters
        self.conn, addr = s.accept() 
        t2 = threading.Thread(target=self.server, args=(addr, s))
        t2.start()

    def server(self, addr, s):
        try:
          # print out the client's address
            print('Connected by', addr)
            while True:
                # Read the content sent by the client
                self.dataReceive = self.conn.recv(1024).decode()
                if(self.dataReceive != ""):
                    friend = self.dataReceive.split("|")[0]
                    action = self.dataReceive.split("|")[1]
                    print(action)
                    if(action == "hit" and friend == "client"):
                        x = int(self.dataReceive.split("|")[2])
                        y = int(self.dataReceive.split("|")[3])
                        self.gui.ButtonHandle(x, y)
                    if(action == "Undo" and friend == "client"):
                        self.gui.Undo(False)
                self.dataReceive = ""
        finally:
            s.close()  # close socket

    def sendData(self, data):
        # send data to server site 
        self.conn.sendall(str("{}|".format(self.name) + data).encode())
