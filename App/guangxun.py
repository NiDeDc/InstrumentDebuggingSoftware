import serial
import serial.tools.list_ports
import time
import config as co
from App import clock

from PyQt5.QtWidgets import QMessageBox

ser = serial.Serial()


def init(self):
    if self.dev == '2':
        self.comboBox_com_2.hide()
        self.pushButton_changer_2.hide()
        self.label_guang_tips.show()
        if clock.ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    elif self.dev == "4":
        self.comboBox_com_2.hide()
        self.pushButton_changer_2.hide()
        self.label_guang_tips.show()
        self.radioButton_pa.hide()
        self.radioButton_ba.setChecked(True)
        if clock.ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    else:
        self.label_guang_tips.hide()
        port_scan(self)
        if ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    # self.timer.timeout.connect(receive_data(self))


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_2.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_2.addItem(por_list[0])
    if select_type(self) == "pa":
        self.comboBox_com_2.setCurrentText(co.read_config("GUANGXUN_PA", "port"))
    else:
        self.comboBox_com_2.setCurrentText(co.read_config("GUANGXUN_BA", "port"))


def set_enabled(self, bol):
    self.comboBox_com_2.setEnabled(not bol)
    self.pushButton_read.setEnabled(bol)
    self.pushButton_set_2.setEnabled(bol)
    if self.dev == '2' or self.dev == "4":
        return None
    self.radioButton_ba.setEnabled(not bol)
    self.radioButton_pa.setEnabled(not bol)


def open_com(self):
    if self.pushButton_changer_2.text() == "打开串口":
        ser.port = self.comboBox_com_2.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_2.setText("关闭串口")
                read_data(self)
                if select_type(self) == "pa":
                    co.set_config("GUANGXUN_PA", "port", self.comboBox_com_2.currentText())
                else:
                    co.set_config("GUANGXUN_BA", "port", self.comboBox_com_2.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        # self.timer.stop()
        try:
            ser.close()
            self.pushButton_changer_2.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def read_data(self):
    data = bytes([0xef, 0xef, 0x03, 0xff, 0x11, 0xf1])
    if self.dev == '2' or self.dev == "4":
        if select_type(self) == 'pa':
            ch_choose = [0x00, 0x00, 0x00, 0x01]
        else:
            ch_choose = [0x00, 0x00, 0x00, 0x03]
        e_data = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x0c] +
                       ch_choose) + data
        print(e_data)
        clock.ser.flushInput()
        clock.ser.write(e_data)
        receive_data(self)
    else:
        print(data)
        # 打开串口接收定时器，周期为2ms
        # self.timer.start(2)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def set_data(self):
    val = int(self.doubleSpinBox_current.value() * 10)
    by1 = val >> 8 & 0xff
    by2 = val & 0xff
    s = 0xef + 0xef + 0x06 + 0xff + 0x48 + 0x01 + by1 + by2
    s &= 0xff
    data = bytes([0xef, 0xef, 0x06, 0xff, 0x48, 0x01, by1, by2, s])
    if self.dev == '2' or self.dev == '4':
        if select_type(self) == 'pa':
            ch_choose = [0x00, 0x00, 0x00, 0x01]
        else:
            ch_choose = [0x00, 0x00, 0x00, 0x03]
        e_data = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x0c] +
                       ch_choose) + data
        print(e_data)
        clock.ser.flushInput()
        clock.ser.write(e_data)
        receive_data(self)
    else:
        print(data)
        # 打开串口接收定时器，周期为2ms
        # self.timer.start(2)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def receive_data(self):
    try:
        time.sleep(0.2)
        if self.dev == '2' or self.dev == "4":
            num = clock.ser.inWaiting()
        else:
            num = ser.inWaiting()
        # self.timer.stop()
    except:
        open_com(self)
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 4:
        if self.dev == '2' or self.dev == "4":
            data = clock.ser.read(num)
        else:
            data = ser.read(num)
        if data[4] == 0x11:
            self.doubleSpinBox_current.setValue((data[5] * 256 + data[6]) / 10)
            tx_power = (data[7] * 256 + data[8]) / 10
            self.lineEdit_power.setText(str(tx_power))
            tx_tem = (data[9] * 256 + data[10]) / 10
            self.lineEdit_temper.setText(str(tx_tem))
        elif data[4] == 0x48:
            QMessageBox.information(self, "提示", "设置成功！")
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")


def select_type(self):
    if self.radioButton_pa.isChecked():
        return "pa"
    elif self.radioButton_ba.isChecked():
        return "ba"


def change_confirm(self):
    if select_type(self) == "pa":
        self.comboBox_com_2.setCurrentText(co.read_config("GUANGXUN_PA", "port"))
    else:
        self.comboBox_com_2.setCurrentText(co.read_config("GUANGXUN_BA", "port"))
