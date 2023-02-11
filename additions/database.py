import json
import os


class db(object):
    def __init__(self , location, needLogs = False):
        self.location = os.path.expanduser(location)
        self.load(self.location)
        self.needLogs = needLogs

    def load(self , location):
       if os.path.exists(location):
           self._load()
       else:
            self.db = {}
       return True

    def _load(self):
        self.db = json.load(open(self.location , "r"))

    def dumpdb(self):
        try:
            json.dump(self.db , open(self.location, "w+"))
            return True
        except:
            return False

    def set(self , key , value):
        try:
            k = self.get(key)
            if type(k) == dict and type(value) == dict:
                k.update(value)
                self.db[str(key)] = k
            else:
                self.db[str(key)] = value
            self.dumpdb()
        except Exception as e:
            if self.needLogs: print("[X] Error Saving Values to Database : " + str(e))
            return False

    def get(self , key):
        try:
            self._load()
            return self.db[key]
        except KeyError:
            if self.needLogs: print("No Value Can Be Found for " + str(key))
            return False

    def delete(self , key):
        if not key in self.db:
            return False
        del self.db[key]
        self.dumpdb()
        return True
    
    def resetdb(self):
        self.db={}
        self.dumpdb()
        return True