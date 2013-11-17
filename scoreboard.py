import sys
import numpy as np
from time import strftime, gmtime
import json

class ScoreBoard:

    """
    Core data looks like:
    data = {"Peter":
                {
                    "Shopping | 2013 Nov 16":
                        (100, -50), 
                    "Eating | 2013 Nov 17":
                        (0, -50)
                },
            "J":
                {
                    "Shopping | 2013 Nov 16":
                        (0, -50),
                    "Eating | 2013 Nov 17":
                        (100, -50)
                }
            }
    """
    def __init__(self, name, people = []):
        self.name = name
        self.data = {}
        self.summary = {}
        for usr in people:
            self.summary[usr] = 0
            self.addMember(usr)
        print "instantiate scoreboard: " + name

    def addMember(self, userName):
        """
        Add a member
        """
        if self.data.has_key(userName):
            print "User exist!"
            return -1
        else:
            print "Add user: " + userName
            self.data[userName] = {}
            self.summary[userName] = 0

    def kickMember(self, userName):
        """
        Calculate how much money a member should pay back to others and kick out
        this user
        To keep track on history, we only add a payback entry to scoreboard but
        not actually delete the user
        """

    def refresh(self):
        """
        calculate current state vector
        """
        users = self.userList()
        for user in users:
            self.summary[user] = self.sumUp(self.data[user])
            
    def sumUp(self, userVector):
        lose = 0
        win = 0
        for entry in userVector:
            win += userVector[entry][0]
            lose += userVector[entry][1]
        score = lose + win
        return score

    def addEntry(self, entry):
        """
        Add an entry to scoreboard
        """
        print "Add entry: " + entry.name
        usersInvolved = entry.data.keys()
        print usersInvolved
        print entry
        for user in self.userList():
            if user in usersInvolved:
                self.data[user][entry.name] = entry.data[user][0]
            else:
                self.data[user][entry.name] = [0, 0]

        self.refresh()
        return self.summary

    def getUserState(self, userName):
        """
        return a user's state
        """
        if self.hasUser(userName):
            return self.data[userName]
        
        return -1

    def hasUser(self, userName):
        """
        return True is user exist
        if yes, return user and user data
        if no, return None
        """
        if self.data.has_key(userName):
            return True
        else:
            return False

    def hasEntry(self, entryName):
        """
        Check whether the scoreboard contains an specific entry
        If yes, return the entry as dict
        If no, return None
        """

    def showState(self):
        """
        return current summary state
        """
        fancyPrint = "\t\t"
        for usr in self.data.keys():
            fancyPrint += "\t"+usr
        fancyPrint += "\n"
        for entry in self.entryList():
            fancyPrint += entry+"\t"
            for usr in self.data.keys():
                fancyPrint += "\t"+str(sum(self.data[usr][entry]))
            fancyPrint += "\n"

        return fancyPrint

    def entryList(self):
        """
        retrieve all entries
        """
        usr = self.userList()
        return self.data[usr[0]].keys()

    def userList(self):
        """
        return all users in scoreboard
        """
        return self.data.keys()

    def clearUp(self):
        """
        calculate how to pay back and clear up
        """
        self.refresh()
        diff = 0
        result = ""
        while self.summary:
            winner = max(self.summary, key = lambda x: self.summary.get(x))
            loser = min(self.summary, key = lambda x: self.summary.get(x))
            diff = self.summary[winner] + self.summary[loser]
            if diff > 0:
                self.summary[winner] = diff
                handover = self.summary.pop(loser)
                print str(loser) + " --> " + str(winner) + ": " + str(abs(handover))
                result += str(loser)+" --> "+str(winner)+": "+str(abs(handover))+"\n"
            elif diff < 0:
                self.summary[loser] = diff
                handover = self.summary.pop(winner)
                print str(loser) + " --> " + str(winner) + ": " + str(abs(handover))
                result += str(loser)+" --> "+str(winner)+": "+str(abs(handover))+"\n"
            else:
                self.summary.pop(loser)
                handover = self.summary.pop(winner)
                print str(loser) + " --> " + str(winner) + ": " + str(abs(handover))
                result += str(loser)+" --> "+str(winner)+": "+str(abs(handover))+"\n"

        return result

class FreshEntry:
    """
    a temporary entry for async features
    {
        "peter":
            [(100, -50), True]
        "J":
            [(0, -50), False]
    }
    """
    def __init__(self, entryName, scoreBoardName):
        currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.name = entryName
        self.scoreBoardName = scoreBoardName
        self.data = {}

    def addValue(self, userName, userValue):
        """
        add a value to entry
        """
        self.data[userName] = [userValue, False]

    def entryIsComplete(self):
        """
        To check whether all users confirmed this entry
        """
        users = self.data.keys()
        for user in users:
            if not self.data[user][1]:
                return False
        return True

    def confirm(self, userName):
        """
        Confirm a shared expenditure for an user
        """
        if self.hasUser(userName):
            self.data[userName][1] = True
        else:
            return -1

        return 0

    def _autoConfirm(self):
        """
        confirm for every fucking user!
        """
        for user in self.data:
            self.confirm(user)
        return 0

    def hasUser(self, userName):
        """
        check user existance
        """
        if self.data.has_key(userName):
            return True
        else:
            return False

if __name__=="__main__":
    test = ScoreBoard("test")
    test.addMember("peach")
    test.addMember("j")
    test.addMember("niklas")
    test.addMember("akis")
    test.addMember("ram")
    test.addMember("wei")
    entry = FreshEntry("ica", "test")
    entry.addValue("peach", (100, -50))
    entry.addValue("j", (0, -10))
    entry.addValue("niklas", (0, -10))
    entry.addValue("akis", (0, -10))
    entry.addValue("ram", (0, -10))
    entry.addValue("wei", (0, -10))
    entry.confirm("peach")
    entry.confirm("j")
    entry.confirm("akis")
    entry.confirm("ram")
    entry.confirm("wei")
    entry.confirm("niklas")
    if entry.entryIsComplete():
        test.addEntry(entry)
    print test.summary
    encoded = json.dumps(test.data, sort_keys=True, indent = 4, separators = (',',';'))
    print encoded
    f = open("test.json",'w')
    f.write(encoded)
    f.close()
    test.clearUp()

    f = open("test.json",'r')
    decoded = json.loads(f.read())
    print decoded

