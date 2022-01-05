import serial
import serial.tools.list_ports
import config as co
import time

from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

ser = serial.Serial()


def init(self):
    port_scan(self)
    if ser.isOpen():
        set_enabled(self, True)
    else:
        set_enabled(self, False)
    self.lineEdit_same_per.setText((co.read_config("CLOCK", "freq")))
    self.lineEdit_same_plaus.setText(co.read_config("CLOCK", "plaus"))
    self.lineEdit_same_timeout.setText(co.read_config('CLOCK', 'timeout'))
    self.lineEdit_same_per.setValidator(QRegExpValidator(QRegExp("[0-9\.]+$")))
    self.lineEdit_same_plaus.setValidator(QRegExpValidator(QRegExp("[0-9\.]+$")))
    self.lineEdit_same_timeout.setValidator(QRegExpValidator(QRegExp("[0-9\.]+$")))


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_8.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_8.addItem(por_list[0])
    self.comboBox_com_8.setCurrentText(co.read_config("CLOCK", "port"))


def set_enabled(self, bol):
    self.comboBox_com_8.setEnabled(not bol)
    self.pushButton_set_sameper.setEnabled(bol)
    self.pushButton_set_sameplaus.setEnabled(bol)
    self.pushButton_set_samtimeout.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer_8.text() == "打开串口":
        ser.port = self.comboBox_com_8.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_8.setText("关闭串口")
                co.set_config("CLOCK", "port", self.comboBox_com_8.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer_8.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def setplaus(self):
    plaus = int(float(self.lineEdit_same_plaus.text())/2.5)
    if plaus > 4294967296 or plaus < 1:
        QMessageBox.warning(self, "提示", "超过设置范围")
    else:
        co.set_config('CLOCK', 'plaus', self.lineEdit_same_plaus.text())
        plaus1 = plaus >> 24 & 0xff
        plaus2 = plaus >> 16 & 0xff
        plaus3 = plaus >> 8 & 0xff
        plaus4 = plaus & 0xff
        data = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x04, plaus1, plaus2,
                      plaus3, plaus4])
        print(data)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def setper(self):
    if float(self.lineEdit_same_per.text()) <= 0.0:
        QMessageBox.warning(self, '提示', '频率必须大于0')
        return None
    per = int(1.0 / float(self.lineEdit_same_per.text()) * 10.0 ** 9.0 / 2.5)
    if 4294967296 < per or per < 1:
        QMessageBox.warning(self, '提示', '超过设置范围')
    else:
        co.set_config('CLOCK', 'freq', self.lineEdit_same_per.text())
        per1 = per >> 24 & 0xff
        per2 = per >> 16 & 0xff
        per3 = per >> 8 & 0xff
        per4 = per & 0xff
        data = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x00, per1, per2, per3,
                      per4])
        print(data)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def setout(self):
    timeout = int(float(self.lineEdit_same_timeout.text())/20 * 10 ** 6)
    if timeout > 4294967296 or timeout < 1:
        QMessageBox.warning(self, '提示', '超过设置范围')
    else:
        co.set_config('CLOCK', 'timeout', self.lineEdit_same_timeout.text())
        timeout1 = timeout >> 24 & 0xff
        timeout2 = timeout >> 16 & 0xff
        timeout3 = timeout >> 8 & 0xff
        timeout4 = timeout & 0xff
        data = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x08, timeout1, timeout2,
                      timeout3, timeout4])
        print(data)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def receive_data(self):
    try:
        time.sleep(0.3)
        num = ser.inWaiting()
        # self.timer.stop()
    except:
        self.open_com(self)
        return None
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num == 18:
        data = ser.read(num)
        print(data)
        if data[17] == 0x00:
            QMessageBox.information(self, "提示", "配置成功")
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")
