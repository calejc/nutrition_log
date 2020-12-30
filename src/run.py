#!/usr/bin/env python3
import sys, sqlite3, datetime, data
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from day import Day
from week import Week
from layout import Ui_MainWindow



class Main_App(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(Main_App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet("""
            QTabWidget, QMainWindow{
                background: rgb(155,155,155);
            }
            QLabel#weight_label{
                color:red;
            }
            
        """)
        self.ui.date_input.setDate(QDate.currentDate().addDays(-1))
        self.ui.save_button.clicked.connect(self.test_function)
        # self.ui.refresh.clicked.connect(self.snapshot)
        # self.snapshot()


    def reset(self):
        self.ui.date_input.setDate(QDate.currentDate())
        self.ui.weight_input.clear()
        self.ui.calories_input.clear(),
        self.ui.protein_input.clear(),
        self.ui.carbs_input.clear(),
        self.ui.burned_input.clear(),
        self.ui.steps_input.clear(),
        self.ui.sleep_input.clear(),

    def sql_test(self):
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        c.execute("select * from picture limit 1")
        results = c.fetchall()

        byte_array = QByteArray(results[0][1])
        pixmap = QPixmap()
        pixmap.loadFromData(byte_array, "JPG")


        # -------------- #
        #  RESIZE IMAGE  #
        # -------------- #
        scaled = pixmap.scaled(self.ui.pic.size(), Qt.KeepAspectRatio, transformMode = Qt.SmoothTransformation)
        self.ui.pic.setMaximumSize(scaled.size())
        self.ui.pic.setScaledContents(True)
        self.ui.pic.setPixmap(pixmap)


        # ---------------- #
        #  INSERT PICTURE  #
        # ---------------- #
        # conn = sqlite3.connect("test.db")
        # c = conn.cursor()
        # try:
        #     today = QDate.currentDate().toJulianDay()
        #     img_binary = self.read_in_picture("imgs/progress_11302020.jpg") 
        #     c.execute(
        #         "INSERT INTO picture (date, picture) VALUES (?, ?)", (today, img_binary)
        #     )
        #     conn.commit()
        # except sqlite3.Error as e:
        #     print(e)



    def read_in_picture(self, filepath):
        with open(filepath, 'rb') as f:
            k = f.read()
        try:
            return k 
        except:
            return None

    def test_function(self):
        day = Day(
            DATE = self.ui.date_input.date().toJulianDay(),
            WEIGHT = self.ui.weight_input.text(),
            CALORIES = self.ui.calories_input.text(),
            PROTEIN = self.ui.protein_input.text(),
            CARBS = self.ui.carbs_input.text(),
            STEPS = self.ui.steps_input.text(),
            BURNED = self.ui.burned_input.text(),
            SLEEP = self.ui.sleep_input.text(),
        )
        day.save()
        self.reset()
        # self.snapshot()

    def snapshot(self):
        today = QDate.currentDate().toJulianDay()
        week_one = Week(today, data.Day_Range.WEEK_ONE_RANGE.value).get_data()
        week_two = Week(today, data.Day_Range.WEEK_TWO_RANGE.value).get_data()
        week_three = Week(today, data.Day_Range.WEEK_THREE_RANGE.value).get_data()
        weekly_data = [week_one, week_two, week_three]
        headers = []
        for i, w in enumerate(weekly_data):
            for n, k in enumerate(w.items()):
                headers.append(k[0]) if k[0] not in headers else headers
                item = QTableWidgetItem(str(k[1])) if not isinstance(k[1], tuple) else QTableWidgetItem("{} - {}".format(k[1][0], k[1][0]))
                self.ui.snapshot_table.setItem(i, n, item)
        self.ui.snapshot_table.setHorizontalHeaderLabels(headers)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main_App()
    ui.show()
    sys.exit(app.exec_())