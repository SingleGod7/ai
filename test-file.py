import os
import time 

localtime = time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime())
if not os.path.exists('data'):
    os.mkdir('data')
    f = open('./data/%s-experiment.txt'%localtime,'w')

class Observer():
    def __init__(self, parameters, waitingTime):
        self.parameters = parameters
        self.waitingTime = waitingTime

    def Observe(self):  #定义单次探测过程
        for i in range(self.parameters):
            a = os.popen("ls" + self.parameters[i])
            #加入警告功能
            print a.read()
            #f.write(self.parameters[i] + ':' + str(a) + '   ')
        f.write('\n')

    def start(self):  #定义整体循环
        while (True):
            Observe()
            time.sleep(self.waitingTime)            

Observer1 = Observer([oscA，ocsB],1)
Observer1.start() 
