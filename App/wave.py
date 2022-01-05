import serial
import serial.tools.list_ports
import time
import config as co

from PyQt5.QtWidgets import QMessageBox

ser = serial.Serial()

amplitude_dict = {0: '9.2V',
                  1: '10.4V',
                  2: '12.4V',
                  3: '14.8V',
                  4: '17.2V',
                  5: '19.6V',
                  6: '22.0V',
                  7: '24.0V',
                  8: '25.6V',
                  9: '27.6V',
                  10: '29.2V',
                  11: 'xx',
                  12: 'xx',
                  13: 'xx',
                  14: 'xx',
                  15: 'xx',
                  16: 'xx',
                  17: 'xx',
                  18: 'xx',
                  19: 'xx',
                  20: 'xx',
                  21: 'xx',
                  22: 'xx',
                  23: 'xx',
                  24: 'xx',
                  25: 'xx'}


def init(self):
    port_scan(self)
    if ser.isOpen():
        set_enabled(self, True)
    else:
        set_enabled(self, False)
    # self.timer.timeout.connect(receive_data(self))


# 扫描可用串口
def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_5.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_5.addItem(por_list[0])
    self.comboBox_com_5.setCurrentText(co.read_config("WAVE", "port"))


def open_com(self):
    if self.pushButton_changer_5.text() == "打开串口":
        ser.port = self.comboBox_com_5.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_5.setText("关闭串口")
                co.set_config("WAVE", "port", self.comboBox_com_5.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        # self.timer.stop()
        try:
            ser.close()
            self.pushButton_changer_5.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def set_enabled(self, bol):
    self.comboBox_com_5.setEnabled(not bol)
    self.pushButton.setEnabled(bol)
    self.pushButton_amplitude.setEnabled(bol)
    self.pushButton_read_centervol.setEnabled(bol)
    self.pushButton_set_centervol.setEnabled(bol)
    self.pushButton_read_amplitude.setEnabled(bol)
    self.pushButton_wave_changer.setEnabled(bol)


def send_wave(self):
    if self.comboBox_wave.currentIndex() == 0:
        wave_data = "01"
    elif self.comboBox_wave.currentIndex == 1:
        wave_data = "02"
    else:
        wave_data = "03"
    freq_data = int(self.spinBox_freq_2.value())
    s = 0xCC + 0x55 + 0x07 + 0xff + int(wave_data, 16) + (freq_data >> 24 & 0xff) + (freq_data >> 16 & 0xff) + \
        (freq_data >> 8 & 0xff) + (freq_data & 0xff)
    s = s & 0xff
    data = bytes([0xCC, 0x55, 0x07, 0xFF, int(wave_data, 16)]) + bytes([freq_data >> 24 & 0xff,
                                                                        freq_data >> 16 & 0xff,
                                                                        freq_data >> 8 & 0xff,
                                                                        freq_data & 0xff]) + bytes([s])
    print(data)
    # 打开串口接收定时器，周期为2ms
    # self.timer.start(2)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def read_amplitude(self):
    s = 0xCC + 0x55 + 0x03 + 0xff + 0x05
    s = s & 0xff
    data = bytes([0xcc, 0x55, 0x03, 0xff, 0x05, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def send_amplitude(self):
    amplitude = self.spinBox_amplitude.value()
    s = 0xCC + 0x55 + 0x04 + 0xff + 0x04 + amplitude
    s = s & 0xff
    data = bytes([0xcc, 0x55, 0x04, 0xff, 0x04, amplitude, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def read_vol(self):
    s = 0xcc + 0x55 + 0x03 + 0xff + 0x07
    s = s & 0xff
    data = bytes([0xcc, 0x55, 0x03, 0xff, 0x07, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def set_vol(self):
    vol = int(self.doubleSpinBox_centervol.value() * 1000)
    s = 0xCC + 0x55 + 0x05 + 0xff + 0x06 + (vol >> 8 & 0xff) + (vol & 0xff)
    s = s & 0xff
    data = bytes([0xcc, 0x55, 0x05, 0xff, 0x06, vol >> 8 & 0xff, vol & 0xff, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def changer(self):
    if self.pushButton_wave_changer.text() == "关闭":
        com = 0x00
        self.pushButton_wave_changer.setText("启动")
    else:
        com = 0x01
        self.pushButton_wave_changer.setText("关闭")
    s = 0xcc + 0x55 + 0x04 + 0xff + 0x08 + com
    s = s & 0xff
    data = bytes([0xcc, 0x55, 0x04, 0xff, 0x08, com, s])
    print(data)
    ser.flushInput()
    ser.write(data)
    receive_data(self)


def receive_data(self):
    try:
        time.sleep(1.6)
        num = ser.inWaiting()
        # self.timer.stop()
    except:
        self.open_com(self)
        return None
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 4:
        data = ser.read(num)
        print(data)
        # self.timer.stop()
        if data[0] == 0xcc and data[1] == 0x55:
            if data[4] == 0x07:
                self.doubleSpinBox_centervol.setValue((data[5] * 256 + data[6]) / 1000)
            elif data[4] == 0x05:
                self.spinBox_amplitude.setValue(data[5])
            elif data[4] <= 0x08:
                QMessageBox.information(self, "提示", "设置成功")
            else:
                QMessageBox.critical(self, "错误", "发送指令有误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")

