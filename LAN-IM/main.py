# coding:utf-8
# author: Peter Schmidt
# Last Modified: 2017/09/18
# 


import sys
import time
import argparse
from vchat import Video_Server, Video_Client

parser = argparse.ArgumentParser()

parser.add_argument('--shost', type=str, default='127.0.0.1')
parser.add_argument('--sport', type=int, default=10087)
parser.add_argument('--sversion', type=int, default=4)
# parser.add_argument('--rhost', type=str, default='127.0.0.1')
# parser.add_argument('--rport', type=int, default=10087)
# parser.add_argument('--rversion', type=int, default=4)
parser.add_argument('--noself', type=bool, default=False)
parser.add_argument('--level', type=int, default=1)

args = parser.parse_args()

sIP = args.shost
sPORT = args.sport
sVERSION = args.sversion
# rIP = args.rhost
# rPORT = args.rport
# rVERSION = args.rversion
SHOWME = args.noself
LEVEL = args.level

if __name__ == '__main__':
    vclient = Video_Client(sIP, sPORT, sVERSION, SHOWME, LEVEL)
    vserver = Video_Server(sIP, sPORT+1, sVERSION)
    vclient.start()
    vserver.start()
    while True:
        time.sleep(1)
        if not vserver.isAlive() or not vclient.isAlive():
            print("Video connection lost...")
            sys.exit(0)
        # if not aserver.isAlive() or not aclient.isAlive():
        #     print("Audio connection lost...")
        #     sys.exit(0)