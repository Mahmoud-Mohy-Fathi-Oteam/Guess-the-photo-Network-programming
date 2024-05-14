import os
from threading import Thread
import time


def server():
    os.system('python server.py')

def client():
    os.system('python client.py')

Thread(target = server).start()
time.sleep(1)
Thread(target = client).start()