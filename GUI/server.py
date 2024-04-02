import socket, threading, dash
from collections import defaultdict
from dash import dcc, html
import plotly.express as px

# init the elements of the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8050))
server_socket.listen()
connection, address = server_socket.accept()

while connection: # while the client is still connected
    BUFFER_SIZE = 1024
    # receive msg_len so we know how long each message should be
    header = connection.recv(4) # recv receives data on a socket and stores it in buffer
    if not header: break # if you're not receiving the length then break the loop 
    
    msg_len = int.from_bytes(header[0:4], byteorder="big") 
    chunks = []
    bytes_recd = 0
    while bytes_recd < msg_len:
        chunk = connection.recv(min(msg_len - bytes_recd, BUFFER_SIZE))
        if not chunk: raise RuntimeError("ERROR")
        chunks.append(chunk)
        bytes_recd += len(chunk) 
    
    data = b"".join(chunks) # this joins all junks received from the input
    
    d = defaultdict(int)
    decoded_data = data.decode('utf-8')
    d_len = len(decoded_data)
    d[decoded_data] = d_len

    # use plotly to plot the values from the dictionary in real time




# check if you need an if __name__ == "__main__" statement
