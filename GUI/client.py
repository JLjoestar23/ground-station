import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # use TCP protocol to instance the socket
client_socket.connect(('127.0.0.1', 8050))
while True:
    string_data = input('Please give me a string to send. (type exit to quit)')
    if string_data == "exit":
        break 
    byte_data = string_data.encode('utf-8') # send string data to server as encoded bytes
    client_socket.sendall(byte_data)