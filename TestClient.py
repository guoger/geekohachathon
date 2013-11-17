import sys
import socket
import json

if __name__=="__main__":
    f = open("init.json", 'r')
    initData = f.read()
    f.close()
    f = open("entry.json", 'r')
    entryData = f.read()
    f.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = ("127.0.0.1", 8181)
    sock.connect(address)
    sock.send(initData)
    sock.send("|")
    sock.send(entryData)
    sock.close()
