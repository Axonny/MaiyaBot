import json

class Config():


    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as fh:
            self.data = json.load(fh)
        self._token = None
        self._token = self.data["token"]

    def save(self):
        with open('config.json', 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(self.data,indent=2,ensure_ascii=False))

    def getData(self,numberOfWeek):
        param = self.numToWeek(numberOfWeek)
        return self.data[param]

    def getDataStr(self,str):
        return self.data[str]

    @property
    def token(self):
        if(not self._token):
            raise ValueError("token is null")
        return self._token

    def numToWeek(self,n):
        if n == 0: return "mon"
        if n == 1: return "tue"
        if n == 2: return "wed"
        if n == 3: return "thu"
        if n == 4: return "fri"
        if n == 5: return "sat"
        if n == 6: return "san"
        raise ValueError("Incorrect Number")
