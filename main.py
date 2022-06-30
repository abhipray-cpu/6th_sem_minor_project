from PyQt5 import QtWidgets, uic
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os
from threading import Thread
import time
import csv
from datetime import datetime
try:
    # Fetch the service account key JSON file contents
    cred = credentials.Certificate('./configKey.json')
    # Initialize the app with a service account, granting admin privileges
    firebase_admin.initialize_app(cred, {
        'databaseURL': f"{os.environ['DATABASE_URI']}"
    })
    # declaring the collection objects
    values = db.reference('/pressure')
    print(values.get())
except Exception as e:
    print(e)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.stopThreads = False
        self.pressureArr = []
        # Load the UI Page
        uic.loadUi('design.ui', self)
        self.pushButton.clicked.connect(self.create_CSV)

    def updateChart(self):
        y_axis = []
        x_axis = []
        for i in range(1, len(self.pressureArr)+1):
            x_axis.append(i)
        for val in self.pressureArr:
            y_axis.append(val)
        self.plot.plot(x_axis, y_axis, pen=pg.mkPen('w', width=1))

    def updateChartUtil(self):
        while 1 == 1:
            self.updateChart()
            time.sleep(1)
            if self.stopThreads:
                break

    def addData(self):
        reading = values.get()
        print(reading)
        self.pressureArr.append(reading)


    def appendData(self):
        while 1 == 1:
            self.addData()
            time.sleep(1)
            if self.stopThreads:
                break

    def create_CSV(self):
        try:
            file = open('data.csv', 'w+', newline='')
            # writing the data into the file
            with file:
               write = csv.writer(file)
               data=[]
               for val in self.pressureArr:
                   data_append=[]
                   data_append.append(val);
                   data.append(data_append)
               write.writerows(data)
        except Exception as e:
            print(e)

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads=False
    Thread(target=main.updateChartUtil).start()
    Thread(target=main.appendData).start()
    Thread(target=main.show()).start()
    Thread(target=main.create_CSV).start()
    sys.exit(exitApp())

def exitApp():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.stopThreads = True
    app.exec_()



if __name__ == '__main__':
    main()
