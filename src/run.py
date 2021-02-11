#!/usr/bin/env python3
import sys, sqlite3, datetime, data
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from day import Day
from week import Week
from layout import Ui_MainWindow
from grid_widgets import HeaderWidget
from table_model import TableModel



class Main_App(QMainWindow, Ui_MainWindow):

    DB_FILE_PATH = '/home/cale/Dropbox/code/python/fitness_app/src/db.db'

    def __init__(self):
        super(Main_App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet("""
            QTabWidget, QMainWindow{
                background: rgb(155,155,155);
            }
            QLineEdit{
                border: 1px solid black;
            }
            
        """)
        self.ui.date_input.setDate(QDate.currentDate().addDays(-1))
        self.populate()
        self.ui.date_input.dateChanged.connect(self.populate)
        self.ui.save_button.clicked.connect(self.save_daily)
        self.weekly_data()

    def populate(self):
        DATE = self.ui.date_input.date().toJulianDay()
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()
        c.execute("select * from day where date like ?", [DATE])
        results = c.fetchall()
        if len(results) > 0:

            self.setStyleSheet("""
                QTabWidget, QMainWindow{
                    background: rgb(155,155,155);
                }
                QLineEdit{
                    border: 1px solid red;
                }
            """)
            r = [i for i in results[0]]
            for i,v in enumerate(r):
                if v is None:
                    r[i] = ""
            self.ui.weight_input.setText(str(r[1]))
            self.ui.calories_input.setText(str(r[2]))
            self.ui.protein_input.setText(str(r[3]))
            self.ui.carbs_input.setText(str(r[4]))
            self.ui.steps_input.setText(str(r[5]))
            self.ui.burned_input.setText(str(r[6]))
            self.ui.sleep_input.setText(str(r[7]))
        else:
            self.reset(setDate=False)


    def overwrite_popup(self, day):
        date = self.ui.date_input.date().toString("MM/dd/yyyy")
        msg = QMessageBox()
        msg.setText("Database already contains an entry for {DATE}.\nOverwrite data?".format(DATE=date))
        msg.addButton(QPushButton("Overwrite"), QMessageBox.YesRole)
        msg.addButton(QPushButton("Discard"), QMessageBox.NoRole)
        x = msg.exec_()
        if x == 0:
            day.update()
        

    def reset(self, setDate):
        self.setStyleSheet("""
            QTabWidget, QMainWindow{
                background: rgb(155,155,155);
            }
            QLineEdit{
                border: 1px solid black;
            }
            
        """)
        if setDate:
            self.ui.date_input.setDate(QDate.currentDate())
        self.ui.weight_input.clear()
        self.ui.calories_input.clear()
        self.ui.protein_input.clear()
        self.ui.carbs_input.clear()
        self.ui.burned_input.clear()
        self.ui.steps_input.clear()
        self.ui.sleep_input.clear()

    def get_image(self):
        conn = sqlite3.connect(self.DB_FILE_PATH)
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
        conn = sqlite3.connect("test.db")
        c = conn.cursor()
        TEST_IMG_FILE = "imgs/progress_11302020.jpg"
        try:
            today = QDate.currentDate().toJulianDay()
            img_binary = self.read_in_picture(TEST_IMG_FILE) 
            c.execute(
                "INSERT INTO picture (date, picture) VALUES (?, ?)", (today, img_binary)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)

    def read_in_picture(self, filepath):
        with open(filepath, 'rb') as f:
            k = f.read()
        try:
            return k 
        except:
            return None

    def save_daily(self):
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
        if day.find_by_date() is not None:
            self.overwrite_popup(day)
        else:
            day.save()
        self.reset(setDate=True)
        self.weekly_data()

    def weekly_data(self):
        today = QDate.currentDate().toJulianDay()
        today_nice = QDate.currentDate().toString("MM/dd/yyyy")
        conn = sqlite3.connect(self.DB_FILE_PATH)
        c = conn.cursor()
        c.execute("select * from day order by date limit 1")
        r = c.fetchall()
        latest_date = r[0][0]
        weeks = ((today - latest_date)//7)+1
        weekly_data = []
        for w in range(weeks):
            d1 = 7 + (7*w)
            d2 = 1 + (7*w)
            new_week = Week(today, [d2, d1]).get_data()
            if new_week:
                weekly_data.append(new_week)

        headers = []
        wk_data = []
        for i, w in enumerate(weekly_data):
            row = [v for v in w.values()]
            date_rng = "{} - {}".format(row[0][0], row[0][1])
            row[0] = date_rng
            wk_data.append(row)
            for n, k in enumerate(w.items()):
                header = k[0].replace("_", " ").upper()
                headers.append(header) if header not in headers else headers
        
        model = TableModel(wk_data, headers)
        self.ui.weekly_table.setModel(model)
        self.ui.weekly_table.resizeColumnsToContents()
        self.ui.weekly_table.horizontalHeader().setStretchLastSection(True)
        self.ui.weekly_table.verticalHeader().setMinimumSectionSize(60)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main_App()
    ui.show()
    sys.exit(app.exec_())