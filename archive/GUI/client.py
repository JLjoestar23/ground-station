import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # use TCP protocol to instance the socket
client_socket.connect(('127.0.0.1', 8050))
while True:
    string_data = input('Please give me a string to send. (type exit to quit)')
    if string_data == "exit":
        break 
    msg_len = len(string_data.encode('utf-8'))
    header = msg_len.to_bytes(4, byteorder='big')
    byte_data = string_data.encode('utf-8') # send string data to server as encoded bytes
    client_socket.sendall(header + byte_data) # what will this look like? Is it just two strings of bytes concatenated?