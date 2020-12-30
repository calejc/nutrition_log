#!/usr/bin/env python3
import sys, sqlite3, datetime, data
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtCore import *
from day import Day
from week import Week
from ui import Ui_MainWindow
from table_model import TableModel



class Main_App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.date.setDate(QDate.currentDate().addDays(-1))
        self.ui.save.clicked.connect(self.test_function)
        self.ui.refresh.clicked.connect(self.snapshot)
        self.snapshot()


    def reset(self):
        self.ui.date.setDate(QDate.currentDate())
        self.ui.weight_input.clear()
        self.ui.calories_input.clear(),
        self.ui.protein_input.clear(),
        self.ui.carbs_input.clear(),
        self.ui.other_kcal_input.clear(),
        self.ui.steps_input.clear(),
        self.ui.sleep_input.clear(),

    def sql_test(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        c.execute("select * from test_day")
        results = c.fetchall()
        print(results)
        for i in results:
            print(QDate.fromJulianDay(i[0]))

    def test_function(self):
        day = Day(
            DATE = self.ui.date.date().toJulianDay(),
            WEIGHT = self.ui.weight_input.text(),
            CALORIES = self.ui.calories_input.text(),
            PROTEIN = self.ui.protein_input.text(),
            CARBS = self.ui.carbs_input.text(),
            STEPS = self.ui.steps_input.text(),
            CALS_BURNED = self.ui.other_kcal_input.text(),
            SLEEP = self.ui.sleep_input.text(),
        )
        day.save()
        self.reset()
        self.snapshot()

    def snapshot(self):
        today = QDate.currentDate().toJulianDay()
        week_one = Week(today, data.Day_Range.WEEK_ONE_RANGE.value).get_data()
        week_two = Week(today, data.Day_Range.WEEK_TWO_RANGE.value).get_data()
        week_three = Week(today, data.Day_Range.WEEK_THREE_RANGE.value).get_data()
        weekly_data = [x for x in [week_one, week_two, week_three] if x]
        print(len(weekly_data))
        print(weekly_data)
        headers = []
        for i, w in enumerate(weekly_data):
            for n, k in enumerate(w.items()):
                headers.append(k[0]) if k[0] not in headers else headers
                item = QTableWidgetItem(str(k[1])) if not isinstance(k[1], tuple) else QTableWidgetItem("{} - {}".format(k[1][0], k[1][1]))
                self.ui.snapshot_table.setItem(i, n, item)
        self.ui.snapshot_table.setHorizontalHeaderLabels(headers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main_App()
    ui.show()
    sys.exit(app.exec_())