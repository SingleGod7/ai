from bayes_opt import BayesianOptimization
from bayes_opt.logger import JSONLogger
from bayes_opt.event import Events
import time
import socket
import os

pbounds = {'x':(0.2,4),'y':(0.2,4),'z':(0.2,4),'a':(0.1,2),'b':(2,3)}
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',8700))
print('Waiting for connetion........')
global g,sock
g = 0

#打开文件操作对象
localtime = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
if not os.path.exists('data'):
    os.mkdir('data')
f = open('./data/%s-experiment.txt'%localtime,'w')

def black_box_function(x,y,z,a,b):
    x = round(x,2)
    y = round(y,2)
    z = round(z,2)
    a = round(a,2)
    b = round(b,2)
    return simulator(x,y,z,a,b)

def simulator(x,y,z,a,b):
    global g,sock
    if g == 0:
        parameters = [str(x),str(y),str(z),str(a),str(b)]
        parameters = ' '.join(parameters)
        print('Here X = %s'% parameters)
        s.listen(1)
        sock,addr = s.accept()
        c = sock.recv(1024).decode()
        c.split(' ')
        c = float(c[1])
        g+=1
    else:
        parameters = [str(x),str(y),str(z),str(a),str(b)]
        parameters = ' '.join(parameters)
        print('Here X = %s'% parameters)
        sock.send(parameters.encode())
        sock.close()
        s.listen(1)
        sock, addr =s.accept()
        c = sock.recv(1024).decode()
        c = c.split(' ')
        c =float(c[1])
        print('Message from %s:%s'% addr) 
        print('score:%f'% c)
        f.write('Score:'+str(c)+' Parameters:'+parameters+'\n')
        return c


optimizer = BayesianOptimization(
    f = black_box_function,
    pbounds = pbounds,
    verbose = 2,
    random_state = 1, 
)
logger = JSONLogger(path='./data/%s.json'%localtime)
optimizer.subscribe(Events.OPTIMIZATION_STEP, logger)
optimizer.maximize(init_points=2,n_iter=3)
print(optimizer.max)
