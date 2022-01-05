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
    self.spinBox_freq.setValue(float(co.read_config("FENGLI", "freq")))
    self.comboBox_len.setCurrentText(co.read_config("FENGLI", "length"))
    self.spinBox_pulse_delay.setValue(float(co.read_config("FENGLI", "delay")))
    self.comboBox_add.setCurrentText(co.read_config("FENGLI", "add"))
    self.comboBox_chancount.setCurrentText(co.read_config("FENGLI", "chCount"))
    self.pushButton_advance.setText("峰值数据发送⩔")
    self.groupBox_advance.hide()
    self.label_pulse_delay.hide()
    self.spinBox_pulse_delay.hide()


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com.addItem(por_list[0])
    self.comboBox_com.setCurrentText(co.read_config("FENGLI", "port"))


def set_enabled(self, bol):
    self.comboBox_com.setEnabled(not bol)
    self.pushButton_start.setEnabled(bol)
    self.pushButton_set.setEnabled(bol)
    self.pushButton_peadsend.setEnabled(bol)
    self.pushButton_personal.setEnabled(bol)
    self.pushButton_pulse_change.setEnabled(bol)
    self.pushButton_bias.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer.text() == "打开串口":
        ser.port = self.comboBox_com.currentText()
        ser.baudrate = 38400
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer.setText("关闭串口")
                co.set_config("FENGLI", "port", self.comboBox_com.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def start(self):
    global instructions
    if self.pushButton_start.text() == "启动":
        instructions = 0x01
        self.pushButton_start.setText("停止")
    else:
        instructions = 0x00
        self.pushButton_start.setText("启动")
    data = bytes([0xaa, 0x55, 0x7e, 0x01, 0x00, 0x03, 0x11, 0x11, 0x11, 0x11,
                  0x00, instructions, 0x00, 0xff, 0xff, 0x00])
    print(data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(data)


def receive_data(self, index):
    try:
        time.sleep(0.3)
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
        elif data[5] == 0x05:
            QMessageBox.information(self, "提示", "切换成功")
        elif data[5] == 0x04:
            if index == int(self.comboBox_chan.currentText()) - 1:
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
    freq = self.spinBox_freq.value()
    length = int(self.comboBox_len.currentText())
    add = int(self.comboBox_add.currentText())
    if add != 0:
        add = add - 1
    len1 = length >> 8 & 0xff
    len2 = length & 0xff
    chan = [0x01, 0x02, 0x03, 0x04]
    for i in chan:
        if i == self.comboBox_chancount.currentIndex() + 1:
            chancount = i
            break
    co.set_config("FENGLI", "freq", str(freq))
    co.set_config("FENGLI", "length", self.comboBox_len.currentText())
    co.set_config("FENGLI", "add", self.comboBox_add.currentText())
    co.set_config("FENGLI", "chCount", self.comboBox_chancount.currentText())
    by1 = freq >> 8 & 0xff
    by2 = freq & 0xff
    data = bytes([0xaa, 0x55, 0x7e, 0x01,
                  0x00, 0x02,
                  0x11, 0x11, 0x11, 0x11,
                  0x22, 0x22,
                  by1, by2,
                  0x00, 0x0a,
                  0x00, chancount,
                  0x00, 0x00, len1, len2,
                  0x00, add & 0xff,
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
    peak_num = self.spinBox_peak_num.value()
    peak_bytes = [0] * peak_num * 2
    peak_bytes[1] = 6
    peak_num_byte1 = peak_num >> 24 & 0xff
    peak_num_byte2 = peak_num >> 16 & 0xff
    peak_num_byte3 = peak_num >> 8 & 0xff
    peak_num_byte4 = peak_num & 0xff
    for i in range(3, peak_num*2, 2):
        peak_bytes[i] = peak_bytes[i-2] + peak_bytes[i-3] * (2**8) + 10
        peak_bytes[i-1] = peak_bytes[i] >> 8 & 0xff
        peak_bytes[i] = peak_bytes[i] & 0xff
    print(peak_bytes)
    ser.flushInput()
    for i in range(int(self.comboBox_chan.currentText())):
        data = bytes([0xaa, 0x55, 0x7e, 0x01,
                      0x00, 0x04,
                      peak_num_byte1, peak_num_byte2, peak_num_byte3, peak_num_byte4,
                      chan[i]]) + bytes(peak_bytes) + bytes([0x00, 0xFF, 0xFF, 0x00])
        print(data)
        ser.write(data)
        time.sleep(0.5)
        receive_data(self, i)
    # self.setCursor(Qt.ArrowCursor)


def pulsechange(self):
    mode = self.comboBox_pulse_change.currentIndex()
    delaybyte = self.spinBox_pulse_delay.value()/5
    co.set_config("FENGLI", "delay", str(self.spinBox_pulse_delay.value()))
    data = bytes([0xaa, 0x55, 0x7e, 0x01, 0x00, 0x05, 0x11, 0x11, 0x11, 0x11, mode, int(delaybyte),
                  0x00, 0xff, 0xff, 0x00])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self, 1)


def setbias(self):
    if self.comboBox_bias.currentIndex() == 0:
        direction = 1
    else:
        direction = 0
    steps = self.spinBox_bias.value()
    data = bytes([0xaa, 0x55, 0x7e, 0x01, 0x00, 0x07, 0x11, 0x11, 0x11, 0x11, direction, steps,
                  0x00, 0xff, 0xff, 0x00])
    print(data)
    ser.flushInput()
    ser.write(data)
