import serial
import serial.tools.list_ports
import time
from PyQt5.QtWidgets import QMessageBox
import config as co

ser = serial.Serial()
cmd = 0x01
type_i = 0x01


def init(self):
    port_scan(self)
    if ser.isOpen():
        set_enabled(self, True)
    else:
        set_enabled(self, False)


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_9.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_9.addItem(por_list[0])
    self.comboBox_com_9.setCurrentText(co.read_config("POWER", "port"))


def set_enabled(self, bol):
    self.comboBox_com_9.setEnabled(not bol)
    self.pushButton_shutdown.setEnabled(bol)
    self.pushButton_restart.setEnabled(bol)
    self.pushButton_read_12.setEnabled(bol)
    self.pushButton_write_12.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer_9.text() == "打开串口":
        ser.port = self.comboBox_com_9.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_9.setText("关闭串口")
                co.set_config("POWER", "port", self.comboBox_com_9.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer_9.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def get_cmd(self):
    index = self.comboBox_com_10.currentIndex()
    global cmd
    if index == 0:
        cmd = 0x02
    elif index == 1:
        cmd = 0x01
    elif index == 2:
        cmd = 0x03
    elif index == 3:
        cmd = 0x04
    return cmd


def get_type(self):
    index = self.comboBox_com_11.currentIndex()
    global type_i
    if index == 0:
        type_i = 0x02
    elif index == 1:
        type_i = 0x01
    elif index == 2:
        type_i = 0x03
    return type_i


def set_shutdown(self):
    cmm = get_cmd(self)
    s = 0xdd + 0xcc + 0x04 + 0xff + cmm + 0x00
    s &= 0xff
    data = bytes([0xdd, 0xcc, 0x04, 0xff, cmm, 0x00, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def set_restart(self):
    cmm = get_cmd(self)
    if cmm == 0x01 or cmm == 0x02:
        s = 0xdd + 0xcc + 0x04 + 0xff + cmm + 0x01
        s &= 0xff
        data = bytes([0xdd, 0xcc, 0x04, 0xff, cmm, 0x01, s])
    elif cmm == 0x03 or cmm == 0x04:
        s = 0xdd + 0xcc + 0x03 + 0xff + cmm
        s &= 0xff
        data = bytes([0xdd, 0xcc, 0x03, 0xff, cmm, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def set_read(self):
    type_t = get_type(self)
    s = 0xdd + 0xcc + 0x04 + 0xff + 0x05 + type_t
    s &= 0xff
    data = bytes([0xdd, 0xcc, 0x04, 0xff, 0x05, type_t, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def set_write(self):
    type_t = get_type(self)
    re_time = self.spinBox_time.value()
    t1 = re_time >> 8 & 0xff
    t2 = re_time & 0xff
    s = 0xdd + 0xcc + 0x06 + 0xff + 0x06 + type_t + t1 + t2
    s &= 0xff
    data = bytes([0xdd, 0xcc, 0x06, 0xff, 0x06, type_t, t1, t2, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def receive_data(self):
    try:
        time.sleep(0.5)
        num = ser.inWaiting()
        # self.timer.stop()
    except:
        open_com(self)
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 5:
        data = ser.read(num)
        cmm = data[4]
        if cmm == 0x05:
            re_time = data[6] * 256 + data[7]
            self.spinBox_time.setValue(re_time)
        elif cmm == 0x01 or cmm == 0x02:
            status = data[5]
            if status == 0x00:
                QMessageBox.information(self, "提示", "关闭成功！")
            elif status == 0x01:
                QMessageBox.information(self, "提示", "重启成功！")
        elif cmm == 0x03 or cmm == 0x04:
            QMessageBox.information(self, "提示", "重启成功！")
        elif cmm == 0x06:
            QMessageBox.information(self, "提示", "写入成功！")
        elif cmm == 0xff:
            QMessageBox.critical(self, "错误", "命令字错误！")
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")
