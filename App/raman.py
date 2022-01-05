import serial
import serial.tools.list_ports
import time
import config as co
from App import clock

from PyQt5.QtWidgets import QMessageBox

ser = serial.Serial()
is_transfer = co.read_config("RAMAN", "transfer").lower()


def init(self):
    if self.dev == '4' and is_transfer == "true":
        self.comboBox_com_6.hide()
        self.pushButton_changer_6.hide()
        self.label_raman_tips.show()
        self.checkBox.setChecked(True)
        if clock.ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    else:
        self.label_raman_tips.hide()
        self.checkBox.setChecked(False)
        port_scan(self)
        if ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_6.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_6.addItem(por_list[0])
    self.comboBox_com_6.setCurrentText(co.read_config("RAMAN", "port"))


def set_enabled(self, bol):
    self.comboBox_com_6.setEnabled(not bol)
    self.pushButton_read_3.setEnabled(bol)
    self.pushButton_read_4.setEnabled(bol)
    self.pushButton_set_4.setEnabled(bol)
    self.pushButton_set_5.setEnabled(bol)


def transfer_change(self):
    global is_transfer
    if self.checkBox.isChecked():
        self.comboBox_com_6.hide()
        self.pushButton_changer_6.hide()
        self.label_raman_tips.show()
        co.set_config("RAMAN", "transfer", "true")
        is_transfer = 'true'
        if clock.ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    else:
        self.comboBox_com_6.show()
        self.pushButton_changer_6.show()
        self.label_raman_tips.hide()
        co.set_config("RAMAN", "transfer", "false")
        is_transfer = 'false'
        port_scan(self)
        if ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)


def open_com(self):
    if self.pushButton_changer_6.text() == "打开串口":
        ser.port = self.comboBox_com_6.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_6.setText("关闭串口")
                co.set_config("RAMAN", "port", self.comboBox_com_6.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer_6.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def read_data_1(self):
    data = bytes([0xef, 0xef, 0x03, 0xff, 0x11, 0xf1])
    if self.dev == '4' and is_transfer == "true":
        ch_choose = [0x00, 0x00, 0x00, 0x01]
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


def read_data_2(self):
    data = bytes([0xef, 0xef, 0x03, 0xff, 0x12, 0xf2])
    if self.dev == '4' and is_transfer == "true":
        ch_choose = [0x00, 0x00, 0x00, 0x01]
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


def set_data_1(self):
    val = int(self.doubleSpinBox_current_3.value() * 10)
    by1 = val >> 8 & 0xff
    by2 = val & 0xff
    # 拉曼改协议之前 s = 0xef + 0xef + 0x06 + 0xff + 0x48 + 0x01 + by1 + by2
    s = 0xef + 0xef + 0x0a + 0xff + 0x52 + 0x22 + by1 + 0x23 + by2 + 0x20 + 0x0d + 0x15
    s &= 0xff
    data = bytes([0xef, 0xef, 0x0a, 0xff, 0x52, 0x22, by1, 0x23, by2, 0x20, 0x0d, 0x15, s])
    if self.dev == '4' and is_transfer == "true":
        ch_choose = [0x00, 0x00, 0x00, 0x01]
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


def set_data_2(self):
    val = int(self.doubleSpinBox_current_4.value() * 10)
    by1 = val >> 8 & 0xff
    by2 = val & 0xff
    # 拉曼改协议之前 s = 0xef + 0xef + 0x06 + 0xff + 0x48 + 0x02 + by1 + by2
    s = 0xef + 0xef + 0x0a + 0xff + 0x52 + 0x24 + by1 + 0x25 + by2 + 0x20 + 0x0d + 0x15
    s &= 0xff
    data = bytes([0xef, 0xef, 0x0a, 0xff, 0x52, 0x24, by1, 0x25, by2, 0x20, 0x0d, 0x15, s])
    if self.dev == '4' and is_transfer == "true":
        ch_choose = [0x00, 0x00, 0x00, 0x01]
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
        if self.dev == '4' and is_transfer == "true":
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
        if self.dev == '4' and is_transfer == "true":
            data = clock.ser.read(num)
        else:
            data = ser.read(num)
        if data[4] == 0x52:
            QMessageBox.information(self, "提示", "设置成功！")
        elif data[4] == 0x11:
            self.doubleSpinBox_current_3.setValue((data[5] * 256 + data[6]) / 10)
            tx_power = (data[7] * 256 + data[8]) / 10
            self.lineEdit_power_2.setText(str(tx_power))
            tx_tem = (data[9] * 256 + data[10]) / 10
            self.lineEdit_temper_3.setText(str(tx_tem))
        elif data[4] == 0x12:
            self.doubleSpinBox_current_4.setValue((data[5] * 256 + data[6]) / 10)
            tx_power = (data[7] * 256 + data[8]) / 10
            self.lineEdit_power_3.setText(str(tx_power))
            tx_tem = (data[9] * 256 + data[10]) / 10
            self.lineEdit_temper_4.setText(str(tx_tem))
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")
