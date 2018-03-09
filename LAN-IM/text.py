#coding:utf-8
#author:zjs
#last modified:2017/9/19
#
#
from socket import *
import threading
import time


class client(threading.Thread):
	def __init__(self, ip, port, showme, level, version):
		super.__init__(type(self))