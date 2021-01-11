import sqlite3, data
from PyQt5.QtCore import *


class Week():

    def __init__(self, date, days_range):
        self.date_range = None
        self.weight = None
        self.calories  = None
        self.protein = None
        self.carbs = None
        self.steps = None
        self.cals_burned = None
        self.sleep = None

        # Query data and set the class attributes
        self.data(date, days_range)

    def data(self, date, days_range):
        d1, d2 = date - days_range[0], date - days_range[1]
        try:
            z = [list(t) for t in zip(*self.query(d1, d2))]
            self.date_range = tuple([self.date_str(x) for x in [d2, d1]])
            means_list = [round(self.mean(a),1) for i, a in enumerate(z) if i is not 0]
            
            self.weight = means_list[0]
            self.calories  = means_list[1]
            self.protein = means_list[2]
            self.carbs = means_list[3]
            self.steps = means_list[4]
            self.cals_burned = means_list[5]
            self.sleep = means_list[6]
        except IndexError as e:
            return 


    def date_str(self, x):
        return QDate.fromJulianDay(x).toString("MM/dd")


    def mean(self, flist):
        nlst = [a for a in flist if a is not None or not ""]
        if nlst:
            lst = [x for x in nlst if not isinstance(x, str)]
        else:
            print("NONE")
            return None
        try:
            return sum(lst) / len(lst)
        except:
            return 0
    
    
    def get_data(self):
        return None if all(v is None for v in vars(self).values() if not isinstance(v, tuple)) else vars(self)


    def query(self, date_1, date_2):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        try:
            c.execute("select * from day where date between ? and ?", (date_2, date_1))
            return c.fetchall()
        except sqlite3.Error as e:
            print(e)
            return None
