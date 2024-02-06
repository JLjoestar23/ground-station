import socket

HOST = '192.168.4.1' # IP Address of the server
PORT = 4210

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Testing client-server')
    data = s.recv(1024)

print('Received', repr(data))