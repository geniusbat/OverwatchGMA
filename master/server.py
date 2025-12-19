# Simple HTTPS server in one file
import socket
import ssl

ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

#Generate context
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/cert.pem", keyfile="/home/phobos/Documents/Programing/OverwatchGMA/master/certs/key.pem")
context.set_ciphers("@SECLEVEL=1:ALL")

#ssocket = context.wrap_socket(ssocket, server_side=True)


print("TCP over SSL server running at https://0.0.0.0:8443")
ssocket.bind(('0.0.0.0', 8443))
ssocket.listen(5)
try:
    while True:
        conn, addr = ssocket.accept()
        conn = context.wrap_socket(conn, server_side=True)
        try:
            message = conn.recv(1024).decode()
            print(message)
            resp = "YES"#"HTTP/1.1 200 OK\r\nConnection: close\r\nContent-Type: text/plain\r\nGracias"
            conn.send(resp.encode())
        finally:
            print("end")
            conn.shutdown(socket.SHUT_RD)
            #conn.close()
except KeyboardInterrupt:
    ssocket.close()

print("Finished")