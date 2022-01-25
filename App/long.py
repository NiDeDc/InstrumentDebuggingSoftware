import serial
import serial.tools.list_ports
import time
import config as co

from PyQt5.QtWidgets import QMessageBox

ser = serial.Serial()
instructions = 0x01


def init(self):
    port_scan(self)
    if ser.isOpen():
        set_enabled(self, True)
    else:
        set_enabled(self, False)
    self.spinBox_freq_3.setValue(float(co.read_config("LONG", "freq")))
    self.comboBox_len_2.setCurrentText(co.read_config("LONG", "length"))
    self.comboBox_chancount_2.setCurrentText(co.read_config("LONG", "chCount"))
    self.pushButton_advance_2.setText("峰值数据发送⩔")
    self.groupBox_advance_2.hide()


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_7.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_7.addItem(por_list[0])
    self.comboBox_com_7.setCurrentText(co.read_config("LONG", "port"))


def set_enabled(self, bol):
    self.comboBox_com_7.setEnabled(not bol)
    self.pushButton_start_2.setEnabled(bol)
    self.pushButton_set_6.setEnabled(bol)
    self.pushButton_peadsend_2.setEnabled(bol)
    self.pushButton_personal_2.setEnabled(bol)
    self.pushButton_bias_2.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer_7.text() == "打开串口":
        ser.port = self.comboBox_com_7.currentText()
        ser.baudrate = 38400
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_7.setText("关闭串口")
                co.set_config("LONG", "port", self.comboBox_com_7.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer_7.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def start(self):
    global instructions
    if self.pushButton_start_2.text() == "启动":
        instructions = 0x01
        self.pushButton_start_2.setText("停止")
    else:
        instructions = 0x00
        self.pushButton_start_2.setText("启动")
    data = bytes([0xaa, 0x55, 0x7e, 0x01, 0x00, 0x03, 0x11, 0x11, 0x11, 0x11,
                  0x00, instructions, 0x00, 0xff, 0xff, 0x00])
    print(data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(data)


def receive_data(self, index):
    try:
        time.sleep(0.1)
        num = ser.inWaiting()
        # self.timer.stop()
    except:
        open_com(self)
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 5:
        data = ser.read(num)
        print(data)
        if data[5] == 0x02:
            if data[11] == 0x01:
                QMessageBox.information(self, "提示", "配置成功")
            elif data[11] == 0x00:
                QMessageBox.critical(self, "错误", "配置失败")
            else:
                pass
        elif data[5] == 0x04:
            if index == int(self.comboBox_chan_2.currentText()) - 1:
                if data[11] == 0x01:
                    QMessageBox.information(self, "提示", "发送成功")
                elif data[11] == 0x00:
                    QMessageBox.critical(self, "错误", "发送失败")
                else:
                    pass
            else:
                pass
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")


def set_freq(self):
    freq = self.spinBox_freq_3.value()
    length = int(self.comboBox_len_2.currentText())
    len1 = length >> 24 & 0xff
    len2 = length >> 16 & 0xff
    len3 = length >> 8 & 0xff
    len4 = length & 0xff
    # if self.comboBox_len_2.currentIndex() == 0:
    #     length = 32768
    #     len1 = length >> 24 & 0xff
    #     len2 = length >> 16 & 0xff
    #     len3 = length >> 8 & 0xff
    #     len4 = length & 0xff
    # elif self.comboBox_len_2.currentIndex() == 1:
    #     length = 65536
    #     len1 = length >> 24 & 0xff
    #     len2 = length >> 16 & 0xff
    #     len3 = length >> 8 & 0xff
    #     len4 = length & 0xff
    # elif self.comboBox_len_2.currentIndex() == 2:
    #     length = 131072
    #     len1 = length >> 24 & 0xff
    #     len2 = length >> 16 & 0xff
    #     len3 = length >> 8 & 0xff
    #     len4 = length & 0xff
    # else:
    #     pass
    chan = [0x01, 0x02, 0x03, 0x04]
    for i in chan:
        if i == self.comboBox_chancount_2.currentIndex() + 1:
            chancount = i
            break
    co.set_config("LONG", "freq", str(freq))
    co.set_config("LONG", "length", self.comboBox_len_2.currentText())
    co.set_config("LONG", "chCount", self.comboBox_chancount_2.currentText())
    by1 = freq >> 8 & 0xff
    by2 = freq & 0xff
    data = bytes([0xaa, 0x55, 0x7e, 0x01,
                  0x00, 0x02,
                  0x11, 0x11, 0x11, 0x11,
                  0x22, 0x22,
                  by1, by2,
                  0x00, 0x0a,
                  0x00, chancount,
                  len1, len2, len3, len4,
                  0x00, 0x07,
                  0x00, 0x03,
                  0x00, 0xff, 0xff, 0x00])
    print(data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(data)
    receive_data(self, 1)


def send_peak(self):
    chan = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
    # self.setCursor(Qt.WaitCursor)
    peak_num = self.spinBox_peak_num_2.value()
    peak_bytes = [0] * peak_num * 3
    peak_bytes[2] = 6
    peak_num_byte1 = peak_num >> 24 & 0xff
    peak_num_byte2 = peak_num >> 16 & 0xff
    peak_num_byte3 = peak_num >> 8 & 0xff
    peak_num_byte4 = peak_num & 0xff
    for i in range(5, peak_num*3, 3):
        peak_bytes[i] = peak_bytes[i-3] + peak_bytes[i-4] * (2**8) + peak_bytes[i-5] * (2**16) + 10
        peak_bytes[i-2] = peak_bytes[i] >> 16 & 0xff
        peak_bytes[i-1] = peak_bytes[i] >> 8 & 0xff
        peak_bytes[i] = peak_bytes[i] & 0xff
    print(peak_bytes)
    ser.flushInput()
    for i in range(int(self.comboBox_chan_2.currentText())):
        data = bytes([0xaa, 0x55, 0x7e, 0x01,
                      0x00, 0x04,
                      peak_num_byte1, peak_num_byte2, peak_num_byte3, peak_num_byte4,
                      chan[i]]) + bytes(peak_bytes) + bytes([0x00, 0xFF, 0xFF, 0x00])
        print(data)
        ser.write(data)
        time.sleep(0.5)
        receive_data(self, i)
    # self.setCursor(Qt.ArrowCursor)


def setbiaslong(self):
    if self.comboBox_bias_2.currentIndex() == 0:
        direction = 1
    else:
        direction = 0
    steps = self.spinBox_bias_2.value()
    data = bytes([0xaa, 0x55, 0x7e, 0x01, 0x00, 0x07, 0x11, 0x11, 0x11, 0x11, direction, steps,
                  0x00, 0xff, 0xff, 0x00])
    print(data)
    ser.flushInput()
    ser.write(data)
