import threading
import time

from threading import Thread
import snap7
from kivy.config import Config
Config.set('graphics', 'width', 300)
Config.set('graphics', 'height', 300)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label


class PLC():
    def __init__(self):
        self.IP = '192.168.0.17'  # Adress PLC
        self.RACK = 0
        self.SLOT = 2
        self.DB_NUMBER = 1
        self.START_ADRESS = 0
        self.SIZE = 4
        self.plc = snap7.client.Client()

    def plcConnect(self): #Connect PLC
        if not self.plc.get_connected() == True:
            self.plc.connect(self.IP, self.RACK, self.SLOT)
        return self.plc.get_connected()

    def plcDisconncet(self):#Disconnect PLC
        self.plc.disconnect()
        return self.plc.get_connected()

    def plcReadStatus(self):#Read Status
        return self.plc.get_cpu_state()
        #db = self.plc.db_read(self.DB_NUMBER, self.SLOT, self.SIZE)
        #info = int.from_bytes(db[256:258], byteorder='big')  # Decode info 'Int'
        #return info

    def plcReadValue(self):#Read value
        self.db = self.plc.db_read(self.DB_NUMBER, self.SLOT, self.SIZE)
        self.info = int.from_bytes(self.db[0:1], byteorder='big')  # Decode info 'Int'
        return self.info

plc = PLC()#Instance PLC

class Stream(Thread):
    def __init__(self, metka):
        Thread.__init__(self)
        self.metka = metka

    def run(self):
        while True:
            time.sleep(3)
            self.metka.analogRead.text = str(plc.plcReadStatus())
            self.metka.status_value.text = str(plc.plcReadValue())

#GUI Kivi
class Example(App):
    def build(self):
        self.PLC_stream = Stream(self)
        self.PLC_stream.start()

        self.Grd = GridLayout(cols=2)
        self.btnOn = Button(text = 'Connect to PLC',
                            on_press = self.callback)
        self.btnRead = Button(text = 'Read From PLC',
                              on_press = self.ReadValue)
        self.btnOff = Button(text='Disconnect to PLC',
                            on_press=self.PLC_ON)
        self.status = Label()
        self.status_value = Label(text='0')
        self.analogRead = Label(text = '0')

        self.Grd.add_widget(self.btnOn)
        self.Grd.add_widget(self.status)
        self.Grd.add_widget(self.btnOff)
        #self.Grd.add_widget(self.status_off)
        self.Grd.add_widget(self.analogRead)
        self.Grd.add_widget(self.btnRead)
        self.Grd.add_widget(self.status_value)

        return self.Grd

    def callback(self, instance):
        self.status.text = str(plc.plcConnect())

    def PLC_ON(self, instance):
        self.status.text = str(plc.plcDisconncet())

    def ReadFrom(self, instance):
        self.analogRead.text = str(plc.plcReadStatus())

    def ReadValue(self, instance):
        self.status_value.text = str(plc.plcReadValue())




if __name__ == '__main__':
    Example().run()