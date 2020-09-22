import json


class Config():

    def __init__(self):
        with open('config.json', 'r', encoding='utf-8') as fh:
            self.data = json.load(fh)
        self._token = self.data.get("token", None)
        self.days_of_week = ["mon", "tue", "wed", "thu", "fri", "sat", "san"]

    def save(self):
        with open('config.json', 'w', encoding='utf-8') as fh:
            fh.write(json.dumps(self.data, indent=2, ensure_ascii=False))

    def getData(self, number_of_week: int, parity: str = None) -> str:
        param = self.numToWeek(number_of_week)
        if not parity:
            parity = self.getDataStr("current_week")
        return self.data[parity][param]

    def getDataStr(self, str: str) -> str:
        return self.data[str]

    @property
    def token(self) -> str:
        if(not self._token):
            raise ValueError("token is null")
        return self._token

    def numToWeek(self, number_of_week: int) -> None:
        return self.days_of_week[number_of_week]

    def swapParity() -> str:
        parity = self.getDataStr("current_week")
        if(parity == "odd"):
            self.data["current_week"] = "even"
        else:
            self.data["current_week"] = "odd"
        self.save()
