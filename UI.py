import Adafruit_ADS1x15
import sys
from PyQt5.QtGui  import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import threading
from queue import Queue
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

event = Queue()
timeint = time.time()

class Window(QDialog):
           
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle('A2D Data connect')
        self.resize(1600, 700)
        self.index=0
    
        self.MyTable1 = QTableWidget(1,4)
        self.MyTable1.setMaximumSize(400,65)
        self.MyTable2 = QTableWidget(1,4)
        self.MyTable2.setMaximumSize(400,65)
        self.MyTable3 = QTableWidget(1,4)
        self.MyTable3.setMaximumSize(400,65)
        self.MyTable4 = QTableWidget(1,4)
        self.MyTable4.setMaximumSize(400,65)
        
        self.MyTable1.setColumnWidth(0, 90);
        self.MyTable1.setColumnWidth(1, 90);
        self.MyTable1.setColumnWidth(2, 90);
        self.MyTable1.setColumnWidth(3, 90);
        self.MyTable2.setColumnWidth(0, 90);
        self.MyTable2.setColumnWidth(1, 90);
        self.MyTable2.setColumnWidth(2, 90);
        self.MyTable2.setColumnWidth(3, 90);
        self.MyTable3.setColumnWidth(0, 90);
        self.MyTable3.setColumnWidth(1, 90);
        self.MyTable3.setColumnWidth(2, 90);
        self.MyTable3.setColumnWidth(3, 90);
        self.MyTable4.setColumnWidth(0, 90);
        self.MyTable4.setColumnWidth(1, 90);
        self.MyTable4.setColumnWidth(2, 90);
        self.MyTable4.setColumnWidth(3, 90);
                
        self.Button1=QPushButton("Start")
        self.Button2=QPushButton("Stop")
        self.Button1.clicked.connect(self.Start)
        self.Button2.clicked.connect(self.Stop)

        self.ComBox = QComboBox()
        self.ComBox.addItems(["chip1","chip2","chip3","chip4"])
        self.ComBox.currentIndexChanged.connect(self.addParam)

        self.Down_layout = QHBoxLayout()
        self.figure = plt.figure(figsize=(10,5), dpi=120)    
        self.canvas = FigureCanvas(self.figure)

        self.list_view = QListView()
        self.list_view.setWindowTitle('Example List')
        self.list_view.setMinimumSize(400, 400)
        self.model = QStandardItemModel(self.list_view)

        channels = ['channel1','channel2','channel3','channel4']    
        for channel in channels:
            item = QStandardItem(channel)
            item.setCheckable(True)
            self.model.appendRow(item)        
        self.list_view.setModel(self.model)
        self.SampleEdit = QLineEdit()
        self.SampleEdit.setText("10")
 
        self.HeadGroupBox = QGroupBox(u'Chip')
        self.ImgBox = QGroupBox(u'Show Image')
        self.ImgBox.setMaximumSize(1600,700)

        layout = QVBoxLayout()
        self.HeadGroupBoxLayout = QGridLayout()
        self.PlotGroupBoxLayout = QGridLayout()
     
        self.HeadGroupBoxLayout.addWidget(self.MyTable1,1,1)
        self.HeadGroupBoxLayout.addWidget(self.MyTable2,1,2)
        self.HeadGroupBoxLayout.addWidget(self.MyTable3,1,3)
        self.HeadGroupBoxLayout.addWidget(self.MyTable4,1,4)
  
        self.HeadGroupBox.setLayout(self.HeadGroupBoxLayout)
        self.axes = self.figure.add_subplot(111)
        self.axes.set_xlabel('time(s)')
        self.axes.set_ylabel('Sensor data')
        self.PlotGroupBoxLayout.addWidget(self.canvas)
        self.ImgBox.setLayout(self.PlotGroupBoxLayout)
 
        HVBox= QVBoxLayout()
        HVBox.addWidget(QLabel("Choose chip :"))
        HVBox.addWidget(self.ComBox)
        HVBox.addWidget(QLabel("Set Sample :"))
        HVBox.addWidget(self.SampleEdit)                
        HVBox.addWidget(QLabel("Choose Channel :"))
        HVBox.addWidget(self.list_view)
        splitter = QSplitter()
        splitter.addWidget(self.Button1)
        splitter.addWidget(self.Button2)
        splitter.setOrientation(Qt.Horizontal)# horizontal 
        HVBox.addWidget(splitter)
 
        self.Down_layout.addLayout(HVBox)
        self.Down_layout.addWidget(self.ImgBox)#(self.canvas)
        self.PlotGroupBoxLayout.addWidget(self.list_view,0,0)

        layout.addWidget(self.HeadGroupBox)       
        layout.addLayout(self.Down_layout)
        self.setLayout(layout)
        
        
    def Start(self):
        self.SampleEdit.setEnabled(False)
        self.Button1.setEnabled(False)
        Sensor.start()
        self.initUI()

    def Stop(self):
        self.DataThread.stop()
        
    def addParam(self,index):   
        self.index=index
  
    def initUI(self):
    ####Data Thead start####
        
        self.DataThread = UpdateData()
        self.DataThread.update_date.connect(self.updatach)
        self.DataThread.start()
        
    #### plot initial ####
 
        #self.axes.clear()
        #self.axes.grid(True)
        if (int(self.SampleEdit.text())>10):
            max_entries = int(self.SampleEdit.text())
        else:
            max_entries = 10
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)
        self.axis_y2 = deque(maxlen=max_entries)
        self.axis_y3 = deque(maxlen=max_entries)
        self.axis_y4 = deque(maxlen=max_entries)
        self.lineplot1, = self.axes.plot([], [], "ro-",label="c1")
        self.lineplot2, = self.axes.plot([], [], "bo-",label="c2")
        self.lineplot3, = self.axes.plot([], [], "go-",label="c3")
        self.lineplot4, = self.axes.plot([], [], "yo-",label="c4")
        self.axes.set_autoscaley_on(True)

    def PLOT(self, x, y):
        
        self.axis_x.append(x)
        self.axis_y1.append(y[0])
        self.axis_y2.append(y[1])
        self.axis_y3.append(y[2])
        self.axis_y4.append(y[3])
        
        if self.model.item(0).checkState() == Qt.Checked:
            self.lineplot1.set_data(self.axis_x, self.axis_y1)    
        if self.model.item(1).checkState() == Qt.Checked:
            self.lineplot2.set_data(self.axis_x, self.axis_y2)
        if self.model.item(2).checkState() == Qt.Checked:
            self.lineplot3.set_data(self.axis_x, self.axis_y3)
        if self.model.item(3).checkState() == Qt.Checked:
            self.lineplot4.set_data(self.axis_x, self.axis_y4)
            
        self.axes.set_xlim(self.axis_x[0], self.axis_x[-1] + 1e-15)
        self.axes.set_ylim(0,28000)
        self.axes.legend()
        self.axes.relim()
        self.axes.autoscale_view()
        self.canvas.draw()

    def updatach(self, data):
        self.PLOT( time.time()-timeint,data[self.index])
        for i in range(len(data[0])):
            str_data1=str(data[0][i])
            str_data2=str(data[1][i])
            str_data3=str(data[2][i])
            str_data4=str(data[3][i])
            self.MyTable1.setItem(0,i,QTableWidgetItem(str_data1))
            self.MyTable2.setItem(0,i,QTableWidgetItem(str_data2))
            self.MyTable3.setItem(0,i,QTableWidgetItem(str_data3))
            self.MyTable4.setItem(0,i,QTableWidgetItem(str_data4))
           

class UpdateData(QThread):
    update_date = pyqtSignal(list)
    def run(self):       
        while True:
            
            getdata=event.get()
            self.update_date.emit(getdata)
                    
class Read_Sensor_Value_Thread (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      print('initial')

    def run(self):
      print('Sensor get')      

      adc1 =Adafruit_ADS1x15.ADS1115(0x48)
      adc2= Adafruit_ADS1x15.ADS1115(0x49)
      adc3= Adafruit_ADS1x15.ADS1115(0x4A)
      adc4= Adafruit_ADS1x15.ADS1115(0x4B)
      GAIN = 2/3
   
      while True :
        values1=[0]*4
        values2=[0]*4
        values3=[0]*4
        values4=[0]*4
        values=[]
       
        try:
            for i in range(4):
                values1[i]=adc1.read_adc(i, gain=GAIN)
                values2[i]=adc2.read_adc(i, gain=GAIN)
                values3[i]=adc3.read_adc(i, gain=GAIN)
                values4[i]=adc4.read_adc(i, gain=GAIN)
            values.append(values1)
            values.append(values2)
            values.append(values3)
            values.append(values4)
            event.put(values)
            time.sleep(0.01)
        except:
            e = sys.exc_info()[0]
            ShowMsg('Error=' + str(e))
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    Sensor=Read_Sensor_Value_Thread()
    win.show() 
    sys.exit(app.exec_())