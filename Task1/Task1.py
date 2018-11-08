from random import randint
from datetime import datetime, timedelta
from datetime import datetime
import sys
import os
import shutil
from PyQt5 import QtWidgets
from PyQt5 import uic
import threading
import workWithDB

""" Main gui class """
class MainWindow(QtWidgets.QMainWindow):

    NUMBER_OF_YEARS = 5
    DAYS_IN_YEAR = 365
    NUMBER_OF_STRINGS_IN_FILES = 100000

    split = "||"

    INTEGER_MIN_VALUE = 1

    INTEGER_MAX_VALUE = 100000000

    FLOAT_MAX_VALUE = 20
    FLOAT_MIN_VALUE = 1
    NUMBER_OF_SINBOLS_AFTER_COMMA = 8

    JOINED_FILE_NAME = "joined.txt"
    DB_NAME = "mydb.db"

    """ function generate and return random date from last 5 years """
    def getRandomDate(self):
        return (datetime.now() - 
                timedelta(days = randint(0, self.NUMBER_OF_YEARS * self.DAYS_IN_YEAR))).date()

    """ function generate and return sequence of random laters """
    def getRandomLaters(self, count : int, first : str):
        sequency = ""
        for i in range(count):
            ch = ord(first) + randint(0,25)
            if randint(0,1) > 0:
                sequency += chr(ch - 32)
            else:
                sequency += chr(ch)
        return sequency

    """ function generate and return string in specific format """
    def buildString(self):
        return  self.getRandomLaters(count=10, first='а').join((self.split,self.split)) \
                        .join((self.getRandomLaters(count=10, first='a'), randint(self.INTEGER_MIN_VALUE, self.INTEGER_MAX_VALUE).__str__())) \
                        .join((self.split,self.split)) \
                        .join((self.getRandomDate().strftime("%d.%m.%Y"), (randint(self.FLOAT_MIN_VALUE * 10 ** self.NUMBER_OF_SINBOLS_AFTER_COMMA,
                        self.FLOAT_MAX_VALUE * 10 ** self.NUMBER_OF_SINBOLS_AFTER_COMMA) 
                        / 10 ** self.NUMBER_OF_SINBOLS_AFTER_COMMA).__str__().replace('.',',',1))) \
                        .join(('',self.split)) \
                        .join(('','\n'))

    def __init__(self,debug = False):
        self.debug = debug
        self.count = 0
        self.countOfDeletedStrings = 0
        self.dirPath = datetime.now().date().strftime("%d.%m.%Y")
        try:
            os.chdir(self.dirPath)
            os.chdir("..")
            shutil.rmtree(self.dirPath)
            os.makedirs(self.dirPath)
        except :
            os.makedirs(self.dirPath)
            print("make dir")
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("gui_1.ui",self)
        filesList = os.listdir('01.11.2018\\')
        self.btnGenerateFiles.clicked.connect(self.generateFilesButtonController)
        self.btnDeleteFiles.clicked.connect(self.deleteFilesButtonController)
        self.btnGenerateFiles.setVisible(self.debug)
        self.btnDeleteFiles.setVisible(self.debug)
        self.spinBoxNumberOfFiles.setVisible(self.debug)
        self.btnJoin.clicked.connect(self.joinButtonController)
        self.lineEditSubstring.setEnabled(False)
        self.checkBox.stateChanged.connect(self.checkBoxClickedController)
        self.btnImport.clicked.connect(self.importToDB)
        self.btnTest.setEnabled(False)
        self.btnTest.setText("get sum and med")
        self.btnTest.clicked.connect(self.getSumAndMed)
        self.show()

    def getSumAndMed(self):
        res = workWithDB.sumAndMed(self.DB_NAME)
        print(res)

    def importToDB(self):
        t = threading.Thread(target=workWithDB.importToDB,args=(self.DB_NAME,self,self.JOINED_FILE_NAME))
        t.start()

    def generateFilesButtonController(self):
        countOfFiles = self.spinBoxNumberOfFiles.value()
        self.status.showMessage("Waiting ...")
        timeStart = datetime.now().time()
        for numberOfFile in range(countOfFiles):
            fileName = self.dirPath + "\\file_" + str(numberOfFile) + ".txt"
            file = open(fileName, "w")
            for numberOfString in range(self.NUMBER_OF_STRINGS_IN_FILES):
                file.write(self.buildString())
            file.close()
        time = datetime.now().time()
        self.status.showMessage(time.__str__() + " " + timeStart.__str__())
        pass

    def deleteFilesButtonController(self):
        filesList = os.listdir(self.dirPath)
        os.chdir(self.dirPath)
        for file in filesList:
            os.remove(file)

        self.table.setRowCount(0)
        pass
    
    def joinButtonController(self):
        countDeletedStringt = {}
        jointFileName = self.JOINED_FILE_NAME
        jointFile = open(jointFileName, "w")
        if self.debug:
            os.chdir(self.dirPath)
        else:
            os.chdir('01.11.2018')
        fileList = os.listdir()
        self.statusbarMessage('start proccess... wait!')
        for fileName in fileList:
            count = 0
            file = open(fileName, "r+")
            filesStrings = file.readlines()
            for string in filesStrings:
                if string == '':
                    filesStrings.remove(string)
                    continue
                if self.checkBox.isChecked():
                    if string.find(self.lineEditSubstring.text()) != -1:
                        count += 1
                        filesStrings.remove(string)
                    else:
                        jointFile.write(string)
                else:
                    jointFile.write(string)
            countDeletedStringt.update({file.name:count})
            s = sum(countDeletedStringt.values())
            file.seek(0)
            file.truncate()
            file.writelines(filesStrings)
        os.chdir('..')
        self.statusbarMessage('Join was successful! deleted %d strings' % (s))
        print(countDeletedStringt)
        pass

    def checkBoxClickedController(self, state):
        self.lineEditSubstring.setEnabled(state)
        pass

    def statusbarMessage(self, message:str):
        if message != '':
            self.status.showMessage(message)
        else:
            self.status.clearMessage()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    debug = False
    if sys.argv.__len__() > 1:
        debug = True
    ax = MainWindow(debug)
    sys.exit(app.exec_())