from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import pandas as pd
import back.search as ir 
import pprint
import time 
import back.utils.log as log
import traceback

class Ui_MainWindow(object):
    """ UI Layout for Main Application
    docstring here
        :param object: 
    """
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(800, 450))
    
        self.main = QtWidgets.QWidget(MainWindow)
        self.main.setObjectName("main")

        self.gridLayout = QtWidgets.QGridLayout(self.main)
        self.gridLayout.setObjectName("gridLayout")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.graphicsView = QtWidgets.QGraphicsView(self.main)
        self.graphicsView.setInteractive(True)
        self.graphicsView.setObjectName("graphicsView")
        font =  QtGui.QFont("HoloLens MDL2 Assets")
        font.setPointSize(10)
        self.graphicsView.setFont(font)
        
        self.verticalLayout.addWidget(self.graphicsView)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.logo = QtWidgets.QLabel(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.logo.sizePolicy().hasHeightForWidth())
        self.logo.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.logo.setFont(font)
        self.logo.setTextFormat(QtCore.Qt.AutoText)
        self.logo.setIndent(0)
        self.logo.setObjectName("logo")
        self.horizontalLayout.addWidget(self.logo)
        
        spacerItem = QtWidgets.QSpacerItem(17, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout.addItem(spacerItem)
        
        self.lineEdit = QtWidgets.QLineEdit(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 18))
        self.lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        
        spacerItem1 = QtWidgets.QSpacerItem(17, 33, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.horizontalLayout.addItem(spacerItem1)
        
        self.btnSearch = QtWidgets.QPushButton(self.main)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSearch.sizePolicy().hasHeightForWidth())
        self.btnSearch.setSizePolicy(sizePolicy)
        self.btnSearch.setObjectName("btnSearch")
        self.horizontalLayout.addWidget(self.btnSearch)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        
        MainWindow.setCentralWidget(self.main)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.logo.setText(_translate("MainWindow", "Museek"))
        self.btnSearch.setText(_translate("MainWindow", "Search"))

class MainWindow(QtWidgets.QMainWindow):
    """
    docstring here
        :param QtWidgets.QMainWindow: Inherit QMainWindow Class
    """
    def __init__(self):
        """ Initializes the Main Window
        docstring here
            :param self:  
        """  
        super(MainWindow, self).__init__()
        self.setWindowTitle("Museek - Lyric Search!")
        # Setup UI
        self.main = Ui_MainWindow()
        self.main.setupUi(self)
        self.data = pd.read_csv("data/songdata.csv")
        self.ind = ir.loadJSON()
        self.home()

    def extractInfo(self, Results):
        """
        docstring here
            :param self: Class Function 
            :param Results: Requires Results to extract info from main data
            :type Results: Dictionary
            :returns: Doc id's 
            :rtype: list
        """   
        
        row_id = []  
        for row in Results:
            row_id.append(int(row))
        res = self.data.iloc[row_id]
        return res
            
    def viewResults(self, res, cluster, Results):
        """ Prints the Results to the Application Main Window
        docstring here
            :param self: Class 
            :param res: Doc Id's 
            :type res: list
        """   
        
        # Positions
        y = 40
        n, _ = res.shape
        for i in range(0, n):
            b = 0
            # Setup Text Object 
            temp = QtWidgets.QGraphicsTextItem()
            temp.setPos(0, y)
            temp.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
            temp.setOpenExternalLinks(True)
            
            # SetHTML 
            lyr = []
            c = 0
            y1 = 0
            w = 1
            # 2D list
            bold = cluster[Results[i]]
            f = 0
            flag = 0
            for char in res.iloc[i]['text']:
                lyr.append(char)
                c+=1
                """ Make Query Terms Bold"""
                if(char==' '):
                    w += 1
                    for row in bold:
                        for pos in range(0, len(row)):
                            if(w==row[len(row)-1]+1):
                                flag = 1
                            if(flag == 1):
                                lyr.append('</b>')
                            if(w==row[pos   ] and (flag==0)):
                                lyr.append('<b>')
                                break;

                if(c%251==0):
                    lyr.append('<br>')
                    y1+= 8
                   
            lyr.append("<br>")
            lyrstring = "".join(lyr)

            temp.setHtml('<font face="Gotham Medium" size=5><a href="http://lyricsfreak.com'+res.iloc[i]['link']+'">'+res.iloc[i]['song']+' - '
            +res.iloc[i]['artist']+'</a></font>'+'<body><p><font face="Merryweather Regular" size=4>'+lyrstring+'</font><br><p></body>')
            
            # Change y pos and add to scene 
            self.scene.addItem(temp)
            y += 6*y1

    def search(self):
        """ Search Function which runs when search button is pressed 
        docstring here
            :param self: Class 
        """   
        self.scene.clear()
        try: 
            self.scene.clear()
            query = self.main.lineEdit.text()
            _start = time.time()
            results, clusters = ir.search(query, self.ind)
            _end = time.time() - _start
            print(_end)
            res = self.extractInfo(results)
            self.viewResults(res, clusters, results)
        except Exception as e:
            temp = QtWidgets.QGraphicsTextItem("Error! We are working on it!")
            print(str(e.with_traceback()))
            self.scene.addItem(temp)

    def home(self): 
        """
        docstring here
            :param self: Class 
        """  
        
        self.scene = QtWidgets.QGraphicsScene(self)
        self.main.btnSearch.clicked.connect(self.search)

        self.main.graphicsView.setScene(self.scene)
        self.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())