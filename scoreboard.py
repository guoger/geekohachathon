import sys
import numpy as np
from time import strftime, gmtime

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
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.summary = {}

    def addMember(self, userName):
        """
        Add a member
        """
        if self.data.has_key(userName):
            print "User exist!"
            return -1
        else:
            self.data[userName] = {}
            self.summary[userName] = 0

    def kickMember(self, userName):
        """
        Calculate how much money a member should pay back to others and kick out
        this user
        To keep track on history, we only add a payback entry to scoreboard but
        not actually delete the user
        """
        refresh()
        paybackName = "Payback of " + userName
        # Create a fresh entry of payback
        payback = FreshEntry(paybackName, self.name)


    def refresh(self):
        """
        calculate current state vector
        """
        users = userList()
        for user in users:
            self.summary[user] = sumUp(self, self.data[user])
            
    def sumUp(self, userVector):
        lose = 0
        win = 0
        for entry in userVector:
            win += userVector[entry][0]
            lose += userVector[entry][1]
        score = lose + win
        return score

    def addEntry(entry):
        """
        Add an entry to scoreboard
        """
        if not FreshEntry.checkEntry(entryValue):
            print "illegal entry!"
            return -1

        usersInvolved = entryValue.keys()
        
        for user in usersInvolved:
            self.data[user][entryName] = entryValue[user]

        return 0

    def getUserState(userName):
        """
        return a user's state
        """

    def hasUser(userName):
        """
        return True is user exist
        if yes, return user and user data
        if no, return None
        """

    def hasEntry(entryName):
        """
        Check whether the scoreboard contains an specific entry
        If yes, return the entry as dict
        If no, return None
        """

class FreshEntry:
    """
    a temporary entry for async features
    {
        "peter":
            [[100, -50], True]
        "J":
            [[0, -50], False]
    }
    """
    def __init__(self, entryName, scoreBoardName):
        currentTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        self.name = entryName + "|" + currentTime
        self.scoreBoardName = scoreBoardName
        self.entry = {}

    def checkEntry(self, entryValue):
        """
        To check whether an entry is valid by sum them up
        TODO: should be implemented at user end?
        """

    def confirm(userName):
        """
        Confirm a shared expenditure
        """

    def commitEntry(self):
        """
        Entry is complete, add to scoreboard
        """

if __name__=="__main__":
    test = ScoreBoard("test")
    member = "peter"
    test.addMember(member)
    print test


