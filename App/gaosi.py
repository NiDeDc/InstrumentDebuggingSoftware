import serial
import serial.tools.list_ports
import time
import config as co

from PyQt5.QtWidgets import QMessageBox

ser = serial.Serial()


def init(self):
    port_scan(self)
    if ser.isOpen():
        set_enabled(self, True)
    else:
        set_enabled(self, False)
    # self.timer.timeout.connect(receive_data(self))


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_3.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_3.addItem(por_list[0])
    if select_type(self) == "pa":
        self.comboBox_com_3.setCurrentText(co.read_config("GAOSI_PA", "port"))
    else:
        self.comboBox_com_3.setCurrentText(co.read_config("GAOSI_BA", "port"))


def set_enabled(self, bol):
    self.comboBox_com_3.setEnabled(not bol)
    self.pushButton_read_2.setEnabled(bol)
    self.pushButton_set_3.setEnabled(bol)
    self.radioButton_pa_2.setEnabled(not bol)
    self.radioButton_ba_2.setEnabled(not bol)


def open_com(self):
    if self.pushButton_changer_3.text() == "打开串口":
        ser.port = self.comboBox_com_3.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_3.setText("关闭串口")
                read_data(self)
                if select_type(self) == "pa":
                    co.set_config("GAOSI_PA", "port", self.comboBox_com_3.currentText())
                else:
                    co.set_config("GAOSI_BA", "port", self.comboBox_com_3.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        # self.timer.stop()
        try:
            ser.close()
            self.pushButton_changer_3.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def select_type(self):
    if self.radioButton_pa_2.isChecked():
        return "pa"
    elif self.radioButton_ba_2.isChecked():
        return "ba"


def read_data(self):
    if select_type(self) == "pa":
        data = bytes([0xef, 0xef, 0x03, 0xff, 0x11, 0xf1])
        print(data)
        # 打开串口接收定时器，周期为2ms
        # self.timer.start(2)
        ser.write(data)
        receive_data(self)
    elif select_type(self) == "ba":
        data1 = bytes([0xef, 0xef, 0x02, 0x01, 0xe1])
        data2 = bytes([0xef, 0xef, 0x02, 0x0b, 0xeb])
        print(data1)
        print(data2)
        # 打开串口接收定时器，周期为2ms
        # self.timer.start(2)
        ser.flushInput()
        ser.write(data1)
        time.sleep(0.2)
        # self.timer.start(2)
        ser.write(data2)
        receive_data(self)
    else:
        pass


def set_data(self):
    if select_type(self) == "pa":
        val = int(self.doubleSpinBox_current_2.value()*10)
        by1 = val >> 8 & 0xff
        by2 = val & 0xff
        s = 0xef + 0xef + 0x0a + 0xff + 0x52 + 0x22 + by1 + 0x23 + by2 + 0x20 + 0x0d + 0x15
        s = s & 0xff
        data = bytes([0xef, 0xef, 0x0a, 0xff, 0x52, 0x22, by1, 0x23, by2, 0x20, 0x0d, 0x15, s])
        print(data)
        # self.timer.start(2)
        ser.flushInput()
        ser.write(data)
        receive_data(self)
    else:
        val = int(self.doubleSpinBox_current_2.value())
        by1 = val >> 8 & 0xff
        by2 = val & 0xff
        s = 0xef + 0xef + 0x04 + 0x0c + by1 + by2
        s &= 0xff
        data = bytes([0xef, 0xef, 0x04, 0x0c, by1, by2, s])
        print(data)
        # self.timer.start(2)
        ser.flushInput()
        ser.write(data)
        receive_data(self)


def receive_data(self):
    try:
        time.sleep(0.3)
        num = ser.inWaiting()
        # self.timer.stop()
    except:
        open_com(self)
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 2:
        data = ser.read(num)
        print(data)
        if select_type(self) == "pa":
            if data[2] == 0x0b:
                self.doubleSpinBox_current_2.setValue((data[5]*256+data[6])/10)
                tx = (data[9]*256+data[10])/10
                self.lineEdit_temper_2.setText(str(tx))
            elif data[5] == 0x3b:
                QMessageBox.information(self, "提示", "设置成功！")
            else:
                QMessageBox.critical(self, "错误", "串口回复数据错误")
        else:
            if data[3] == 0x01:
                self.doubleSpinBox_current_2.setValue((data[4]*256+data[5])/1)
                tx = (data[13]*256+data[14])/100
                self.lineEdit_temper_2.setText(str(tx))
            # elif data[3] == 0x0b:
            #     tx = (data[4]*256+data[5])/100
            #     self.lineEdit_temper.setText(str(tx))
            elif data[3] == 0x07:
                QMessageBox.information(self, "提示", "设置成功！")
            else:
                QMessageBox.critical(self, "错误", "串口回复数据错误！")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")


def change_confirm(self):
    if select_type(self) == "pa":
        self.comboBox_com_3.setCurrentText(co.read_config("GAOSI_PA", "port"))
    else:
        self.comboBox_com_3.setCurrentText(co.read_config("GAOSI_BA", "port"))
