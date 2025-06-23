import re
from datetime import datetime

class DataType:
    def __init__(self, data):
        self.data = data
        self.type = self.__validation()

    def __validation(self):
        if re.fullmatch(r'^[\w-]+@[\w\.]+\.\w+$', self.data):
            return "email"
        if re.fullmatch(r'^\+7 \d{3} \d{3} \d{2} \d{2}$', self.data):
            return "phone"
        if self.__is_valid_date():
            return "date"
        return "text"

    def __is_valid_date(self):
        try:
            if "." in self.data:
                day, month, year = map(int, self.data.split("."))
            elif "-" in self.data:
                year, month, day = map(int, self.data.split("-"))
            datetime(year=year, month=month, day=day)
            return True
        except Exception:
            return False
