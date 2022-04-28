import socket

server = "170.187.204.77"
port = 22

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))
