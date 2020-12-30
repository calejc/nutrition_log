# Daily object for each calendar day
import sqlite3


class Day():

    def __init__(self, DATE, WEIGHT, CALORIES, PROTEIN, CARBS, STEPS, BURNED, SLEEP):
        self.DATE = DATE
        self.WEIGHT = WEIGHT
        self.CALORIES = CALORIES
        self.PROTEIN = PROTEIN
        self.CARBS = CARBS
        self.STEPS = STEPS
        self.BURNED = BURNED
        self.SLEEP = SLEEP

    def print_day(self):
        print("DATE: {DATE}\nWEIGHT: {WEIGHT}\nCALORIES: {CALORIES}\nPROTEIN: {PROTEIN}\nCARBS: {CARBS}\nSTEPS: {STEPS}\nOTHER CALORIES BURNED: {BURNED}\nSLEEP: {SLEEP}\n".format(
            DATE = self.DATE,
            WEIGHT = self.WEIGHT,
            CALORIES = self.CALORIES,
            PROTEIN = self.PROTEIN,
            CARBS = self.CARBS,
            STEPS = self.STEPS,
            BURNED = self.BURNED,
            SLEEP = self.SLEEP
        ))

    def save(self):
        # print ("{} -- {}".format(type(self.DATE), self.DATE))
        # return 
        # conn = sqlite3.connect("test.db")
        # c = conn.cursor()
        # try:
            # c.execute("select * from test_day where date like ?", [self.DATE])
            # conn.commit()
        # except Error as e:
            # print(e)
            # return None
        # results = c.fetchall()

        if self.find_by_date():
            return None
        else:
            conn = sqlite3.connect("test.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO day (date, weight, calories, protein, steps, burned, sleep) VALUES (?, ?, ?, ?, ?, ?, ?)", (self.DATE, self.WEIGHT, self.CALORIES, self.PROTEIN, self.STEPS, self.BURNED, self.SLEEP)
            )
            conn.commit()
            return True

    def find_by_date(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        c.execute("select * from day where date like ?", [self.DATE])
        conn.commit()
        if len(c.fetchall()) > 0:
            return c.fetchall()
        else:
            return None 