import json
from datetime import datetime

class Database():

    default = {
        "isWork": False,
        "isInputDate": False,
        "isWorkAdd": False,
        "isWorkInput": False,
        "tasks": [],
        "tmpTask": {
            "date": "0.0",
            "data": "Any"
        }
    }

    def __init__(self):
        with open('database.json', 'r', encoding='utf-8') as fh:
            self.data = json.load(fh)

    def save(self):
        with open('database.json', 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(self.data,indent=2,ensure_ascii=False))

    def CheckProfile(self,id):
        try:
            self.data[id]
        except:
            self.data[id] = self.default
            self.save()

    def addDataProfile(self,id,task):
        id = str(id)
        self.CheckProfile(id)
        self.data[id]["tmpTask"]["data"] = task
        self.data[id]["tasks"].append(self.data[id]["tmpTask"])
        self.save()

    def getDataDate(self,id,date):
        id = str(id)
        self.CheckProfile(id)
        res = []
        for task in self.data[id]["tasks"]:
            if(task["date"] == date):
                res.append(task)
        return res

    def IsData(self,id, *args):
        res = []
        for i in args:
            res.append(self.data[str(id)][i])
        return res

    def SetData(self, id, variable: str, value):
        self.data[str(id)][variable] = value
        self.save()

    def SetDateTask(self, id, date):
        id = str(id)
        self.CheckProfile(id)
        self.data[id]["tmpTask"]["date"] = date
        self.save()

    def DelitePastTasks(self,id):
        date = datetime.now()
        d,m = date.day, date.month
        delites = []
        for task in self.data[str(id)]["tasks"]:
            dt,mt = map(int,task["date"].split('.'))
            if(mt < m or (mt == m and dt < d)):
                delites.append(task)
        for i in delites:
            self.data[str(id)]["tasks"].remove(i)
        self.save()


    def DeliteTask(self,id,index):
        self.data[str(id)]["tasks"].pop(index)
        self.save()
