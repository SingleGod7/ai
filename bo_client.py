import socket
import sys

#客户端部分
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
a = sys.argv
a = ' '.join(a)
s.connect(('127.0.0.1',8700))
s.send(a.encode('utf-8'))
c = s.recv(1024).decode().split(' ')
c = [i for i in c if(len(str(i))!=0)]
print(c[0][1:])
print(c[1])
print(c[2])
print(c[3][:-1])
print(c[4])
