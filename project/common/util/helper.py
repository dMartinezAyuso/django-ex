from datetime import date, datetime

class DateHelper:

    def __init__(self, init_date):
        self.init_date = init_date
        if type(init_date) is str:
            self.init_date = datetime.strptime(init_date, "%Y-%m-%d").date()
        self.today_date = date.today()

    def isAfterThan(self, str_new_date):
        new_date = str_new_date
        if type(str_new_date) is str:
            new_date = datetime.strptime(str_new_date, "%Y-%m-%d").date()
        return self.init_date > new_date

    def isBeforeThan(self, str_new_date):
        new_date = str_new_date
        if type(str_new_date) is str:
            new_date = datetime.strptime(str_new_date, "%Y-%m-%d").date()
        return self.init_date < new_date

    def isAfterThanToday(self):
        return self.isAfterThan(self.today_date)

    def isBeforeThanToday(self):
        return self.isBeforeThan(self.today_date)
