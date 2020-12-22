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

    def get_data_str(self, str: str) -> str:
        return self.data[str]

    @property
    def token(self) -> str:
        if(not self._token):
            raise ValueError("token is null")
        return self._token
