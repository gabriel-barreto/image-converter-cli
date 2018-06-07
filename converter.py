#!/usr/bin/python3
#-*- coding:utf-8 -*-

import argparse
import bz2
import base64
import imghdr
import os
import threading
import time
from PIL import Image

parser = argparse.ArgumentParser(
    prog="Img ===> b64", 
    description="Convert image file in base64 string"
)

parser.add_argument(
    '--src',
    required=True,
    help="Path to image file or images folder"
)

parser.add_argument(
    '--size',
    required=False,
    help="Image size"
)

def init():
    if not os.path.exists('./result.txt'):
        os.system('touch result.txt')

def checkSrc(path):
    if not os.path.exists(path):
        raise Exception('Image/Folder path not found!')
    else:
        if os.path.isfile(path):
            return True
        else:
            return False

def join(list, separator = ' '):
    joinned_list = ''
    for item in list:
        joinned_list += str(item) + separator
    return joinned_list[0:(len(joinned_list) - len(separator))]

def convert(target):
    print('Compressing {}...'.format(target))
    image = Image.open(target, mode="r")
    image.thumbnail(size)
    image.save(target)
    print('Resize to {}x{} ... OK!'.format(size[0], size[1]))
    with open(target, 'rb') as target:
        buffer = target.read()
        value = base64.b64encode(buffer)
        result.append(value.decode('utf-8'))
        print('Compressing {}... OK!'.format(target.name))
        return value

class ThreadRunner(threading.Thread):
    def __init__(self, path):
        self.target = path
        threading.Thread.__init__(self)

    def run(self):
        convert(self.target)

result = []
size = [300, 300]
if __name__ == '__main__':
    initTime = time.time()
    init()
    path = parser.parse_args().src
    if (parser.parse_args().size):
        size = [int(size) for size in parser.parse_args().size.split(' ')]

    if (checkSrc(path)):
        convert(path)
    else:
        targets = [el for el in os.listdir(path) if os.path.isfile(os.path.join(path, el))]
        runners = []
        for file in targets:
            t = ThreadRunner(os.path.join(path, file))
            runners.append(t)
            t.start()
        [t.join() for t in runners]

    file = open('./result.txt', 'w')
    file.write(join(result, '\n\n\n\n\n'))
    file.close()
    print('Job is finished in {}s'.format(time.time() - initTime))
