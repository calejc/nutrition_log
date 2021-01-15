# Daily object for each calendar day
import sqlite3


class Day():

    DATABASE_FILE = "db.db"

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
        if not self.find_by_date():
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            c.execute(
                "INSERT INTO day (date, weight, calories, protein, steps, burned, sleep) VALUES (?, ?, ?, ?, ?, ?, ?)", (self.DATE, self.WEIGHT, self.CALORIES, self.PROTEIN, self.STEPS, self.BURNED, self.SLEEP)
            )
            conn.commit()

    def find_by_date(self):
        conn = sqlite3.connect("db.db")
        c = conn.cursor()
        c.execute("select * from day where date like ?", [self.DATE])
        r = c.fetchall()
        if len(r) > 0:
            return r
        else:
            return None 
    
    def update(self):
        pstmt = ""
        conn = sqlite3.connect("db.db")
        c = conn.cursor()
        for i in vars(self):
            if vars(self)[i] and i is not "DATE":
                vstr = "{} = {}, ".format(i.lower(), vars(self)[i])
                pstmt += vstr
        pstmt = pstmt[:-2]
        print("update day set {PSTMT} where date like {DATE}".format(PSTMT=pstmt, DATE=self.DATE))
        c.execute("update day set {PSTMT} where date like {DATE}".format(PSTMT=pstmt, DATE=self.DATE))
        conn.commit()
