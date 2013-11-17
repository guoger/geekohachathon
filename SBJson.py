import json
import scoreboard as sb
import socket
import thread

SBs = {}
entries = {}

def createNewSB(msg):
    """
    create a now scoreboard
    """
    name = msg.get('name')
    users = msg.get('people')
    SBs[name] = sb.ScoreBoard(name, users)
    print SBs[name].summary
    print SBs[name].data

def addEntry(msg):
    """
    add an entry to a scoreboard
    """
    SBName = msg.get("SBName")
    entryName = msg.get("entryName")
    entry = sb.FreshEntry(entryName, SBName)
    usrInvolved = msg.get("items")
    payer = msg.get("payer")
    total = 0
    temp = 0
    for usr in usrInvolved:
        temp = usrInvolved[usr]
        entry.addValue(usr, [0, temp])
        total += temp

    entry.data[payer][0][0] = abs(total)
    # TODO disseminate notification and confirm
    entry._autoConfirm()
    if SBs.has_key(SBName):
        SBs.get(SBName).addEntry(entry)
        print SBs.get(SBName).showState()

def connHandler(conn):
    """
    handling a connection, parse Json message and update scoreboard accordingly
    """
    data = conn.recv(1024)
    raw = data.split("|")
    for data in raw:
        msg = json.loads(data)
        msgType = msg.get("messageType")
        if msgType == "init":
            createNewSB(msg)
        elif msgType == "addEntry":
            addEntry(msg)
        else:
            print "unknown type of message"

    conn.close()


if __name__=="__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 8181))
    sock.listen(5)
    print "Listening on port 8181"
    while True:
        conn, addr = sock.accept()
        print "connect with " + addr[0] + ":" + str(addr[1])
        thread.start_new_thread(connHandler, (conn,))
