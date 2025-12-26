# Simple HTTPS server in one file
import socket
import ssl

class Client():
    host :str
    port :int
    cert :str
    key :str
    context : ssl.SSLContext
    sock : socket.socket

    def __init__(self, host, port, cert, key):
        self.host = host
        self.port = port
        self.cert = cert
        self.key = key
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.sock = self.context.wrap_socket(self.sock)
    
    def connect_send(self,message:str):
        self.sock.connect((self.host,self.port))
        self.sock.send(message.encode())
    
    def close(self):
        self.sock.shutdown(socket.SHUT_WR)

    
    def __str__(self):
        return "Client:{}:{} cert:{}".format(self.host, self.port, self.cert)
    
if __name__ == "__main__":
    cl = Client("0.0.0.0", 8443, "/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", "/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
    cl.connect_send("Hola mundo")
    cl.close()

'''
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
#context.load_cert_chain(certfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", keyfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
#context.set_ciphers("@SECLEVEL=1:ALL")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ssocket = context.wrap_socket(ssocket)

print("TCP over SSL server running at https://0.0.0.0:8443")
ssocket.connect(('0.0.0.0', 8443))
ssocket.send(b"Hola mundo")
print(ssocket.recv(4096).decode())
import time
ssocket.close()
'''