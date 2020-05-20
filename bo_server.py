import socket
import numpy as np
import pickle
import scipy
import combo
import time
import os
#import urllib
#import ssl
#import matplotlib.pyplot as plt

#建立服务器
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1',8700))
print('Waiting for connetion........')

#打开一个文件操作对象
localtime = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
if not os.path.exists('data'):
    os.mkdir('data')
f = open('./data/%s-experiment.txt'%localtime,'w')
#建立进程通讯
class simulator:
    def __call__(self,action):
        X_new = [str(x) for x in X[action,:]]
        X_new = ' '.join(X_new)
        print('Here X = %s'% X_new)
        s.listen(1)
        sock, addr =s.accept()
        c = sock.recv(1024).decode()
        c = c.split(' ')
        c =float(c[1])
        sock.send(X_new.encode())
        print('Message from %s:%s'% addr) 
       
        sock.close()
        f.write(str(c)+' '+X_new+'\n')
        return c
        
#X的范围(0,10v)并初始化
'''
X = np.zeros((100000000,4))
for i in np.arange(0,X.shape[0]):
    arg4 = (i%100)*0.1
    arg3 = ((i//100)%100)*0.1
    arg2 = ((i//10000)%100)*0.1
    arg1 = (i//1000000)*0.1
    X[i] = [arg1,arg2,arg3,arg4]
np.save('dataspace.npy',X)
'''
X = np.load('dataspace.npy')
print('data space already ok!')
#贝叶斯优化
X1 = combo.misc.centering( X )
print('data nomrize ok!')
policy = combo.search.discrete.policy(test_X = X1)
policy.set_seed(0)
res = policy.random_search(max_num_probes=20,simulator=simulator())
res = policy.bayes_search(max_num_probes=80,simulator=simulator(),score='TS',interval=20,num_rand_basis=5000)


#记录所有的传输数据
res.save('./data/%s.npz'% localtime)

#向模型中载入数据
#res = combo.search.discrete.results.history()
#res.load('path-to-npz-file')

