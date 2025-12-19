# Simple HTTPS server in one file
import socket
import ssl

ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_cert_chain(certfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", keyfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
#context.set_ciphers("@SECLEVEL=1:ALL")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE
ssocket = context.wrap_socket(ssocket)

print("TCP over SSL server running at https://0.0.0.0:8443")
ssocket.connect(('0.0.0.0', 8443))
ssocket.send(b"Hola mundo")
print(ssocket.recv(4096).decode())
ssocket.close()