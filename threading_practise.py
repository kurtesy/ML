# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 11:20:23 2018

@author: npatel
"""

from threading import Thread
import time
import gevent

def add(x,y):
#    print(x+y)
    s = 0
    for i in range(100000000):
        s+=i
    return x+y

def sub(x,y):
    print(x-y)
    return x-y

def mul(x,y):
    print(x*y)
    return x*y

def div(x,y):
    print(x/y)
    return x/y

t1=Thread(target=add, args=(2,3))
t2=Thread(target=add, args=(4,5))
t3=Thread(target=add, args=(5,5))
print(dir(gevent))

start_t = time.time()
t1.start()
t3.start()
t2.start()
end_t = time.time()
print('With threads time taken {t}'.format(t=end_t-start_t))

start_t = time.time()
add(2,3)
add(4,5)
add(5,5)
end_t = time.time()
print('Without threads time taken {t}'.format(t=end_t-start_t))