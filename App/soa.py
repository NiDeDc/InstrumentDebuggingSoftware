import serial
import serial.tools.list_ports
import time
import config as co

from PyQt5.QtWidgets import QMessageBox
from App import clock

ser = serial.Serial()


def init(self):
    if self.dev == "2" or self.dev == "4":
        self.comboBox_com_4.hide()
        self.pushButton_changer_4.hide()
        self.label_soa_tips.show()
        if clock.ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
    else:
        self.label_soa_tips.hide()
        port_scan(self)
        if ser.isOpen():
            set_enabled(self, True)
        else:
            set_enabled(self, False)
        # self.timer.timeout.connect(receive_data(self))


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com_4.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_4.addItem(por_list[0])
    self.comboBox_com_4.setCurrentText(co.read_config("SOA", "port"))


def set_enabled(self, bol):
    self.comboBox_com_4.setEnabled(not bol)
    # self.pushButton_open.setEnabled(bol)
    self.pushButton_readtherm.setEnabled(bol)
    # self.pushButton_readpd.setEnabled(bol)
    # self.pushButton_settec.setEnabled(bol)
    # self.pushButton_setdfb.setEnabled(bol)
    self.pushButton_setplaus_tls.setEnabled(bol)
    self.pushButton_readplaus_dts.setEnabled(bol)
    self.pushButton_setplaus_dts.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer_4.text() == "打开串口":
        ser.port = self.comboBox_com_4.currentText()
        ser.baudrate = 9600
        try:
            ser.open()
            if ser.isOpen():
                # 打开串口接收定时器，周期为2ms
                # self.timer.start(2)
                set_enabled(self, True)
                self.pushButton_changer_4.setText("关闭串口")
                co.set_config("SOA", "port", self.comboBox_com_4.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        # self.timer.stop()
        try:
            ser.close()
            self.pushButton_changer_4.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")

# TLS4000

# def open(self):
#     if self.pushButton_open.text() == "打开TEC":
#         self.open_tec()
#         self.pushButton_open.setText("关闭TEC")
#     elif self.pushButton_open.text() == "关闭TEC":
#         self.close_tec()
#         self.pushButton_open.setText("打开TEC")

# def open_tec(self):
#     comn = 0x04
#     data = 0x00
#     self.send_data(comn, data)
#
#
# def close_tec(self):
#     comn = 0x04
#     data = 0x01
#     self.send_data(comn, data)

# def read_datatherm(self):
#     comn = 0x05
#     data = 0
#     send_data(self, comn, data)


# def read_datapd(self):
#     comn = 0x06
#     data = 0
#     send_data(self, comn, data)

# def set_datatec(self):
#     comn = 0x01
#     data = (self.spinBox_tec.value(), self.spinBox_tec_2.value())
#     self.send_data(comn, data)
#
# def set_datadfb(self):
#     comn = 0x02
#     data = self.spinBox_dfb.value()
#     self.send_data(comn, data)


# def set_dataplaus_tls(self):
#     comn = 0x03
#     data = self.spinBox_pulses_tls.value()
#     send_data(self, comn, data)


# DTS
def read_dts_all(self):
    comn = 0xdd
    data = 0
    send_data(self, comn, data)


def set_plaus_dts(self):
    comn = 0xc5
    data = self.spinBox_pulses_dts.value()
    if data > (int(self.comboBox_plaus_times.currentText()) * 255):
        QMessageBox.warning(self, "警告", "超过当前倍数最大限制")
    else:
        data = int(data/int(self.comboBox_plaus_times.currentText()))
        send_data(self, comn, data)


def send_data(self, comn, dat):
    start1 = 0xaa
    start2 = 0x55
    adr = 0xff
    comnd = comn
    data = dat
    if self.dev == '2' or self.dev == "4":
        clock.ser.flushInput()
    else:
        ser.flushInput()
    # if comnd == 0x01:
    #     length = 0x07
    #     by0 = data[0] >> 8 & 0xff
    #     by1 = data[0] & 0xff
    #     by2 = data[1] >> 8 & 0xff
    #     by3 = data[1] & 0xff
    #     s = start1 + start2 + length + adr + comnd + by0 + by1 + \
    #         by2 + by3
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, by0, by1,
    #                  by2, by3, s])
    #     print(msg)
    #     # 打开串口接收定时器，周期为2ms
    #     # self.timer.start(2)
    #     ser.write(msg)
    # elif comnd == 0x02:
    #     length = 0x05
    #     by0 = (data*100) >> 8 & 0xff
    #     by1 = (data*100) & 0xff
    #     s = start1 + start2 + length + adr + comnd + by0 + by1
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, by0, by1, s])
    #     print(msg)
    #     # 打开串口接收定时器，周期为2ms
    #     # self.timer.start(2)
    #     ser.write(msg)
    # elif comnd == 0x03:
    #     length = 0x04
    #     by0 = data & 0xff
    #     s = start1 + start2 + length + adr + comnd + by0
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, by0, s])
    #     print(msg)
    #     # 打开串口接收定时器，周期为2ms
    #     # self.timer.start(2)
    #     ser.write(msg)
    # elif comnd == 0x04:
    #     length = 0x04
    #     s = start1 + start2 + length + adr + comnd + data
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, data, s])
    #     print(msg)
    #     # 打开串口接收定时器，周期为2ms
    #     # self.timer.start(2)
    #     ser.write(msg)
    # elif comnd == 0x05:
    #     length = 0x03
    #     s = start1 + start2 + length + adr + comnd + data
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, s])
    #     print(msg)
    #     # 打开串口接收定时器，周期为2ms
    #     # self.timer.start(2)
    #     ser.write(msg)
    if comnd == 0xc5:
        length = 0x04
        s = start1 + start2 + length + adr + comnd + data
        s = s & 0xff
        msg = bytes([start1, start2, length, adr, comnd, data, s])
        if self.dev == '2' or self.dev == "4":
            e_msg = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00,
                           0x00, 0x02]) + msg
            print(e_msg)
            clock.ser.write(e_msg)
        else:
            print(msg)
            # 打开串口接收定时器，周期为2ms
            # self.timer.start(2)
            ser.write(msg)
    # elif comnd == 0xc7:
    #     length = 0x04
    #     s = start1 + start2 + length + adr + comnd + data
    #     s = s & 0xff
    #     msg = bytes([start1, start2, length, adr, comnd, data, s])
    #     print(msg)
    #     ser.write(msg)
    elif comnd == 0xdd:
        length = 0x03
        s = start1 + start2 + length + adr + comnd + data
        s = s & 0xff
        msg = bytes([start1, start2, length, adr, comnd, s])
        if self.dev == '2' or self.dev == "4":
            e_msg = bytes([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xFF, 0x00, 0x00, 0x00, 0x0c, 0x00, 0x00,
                           0x00, 0x02]) + msg
            print(e_msg)
            clock.ser.write(e_msg)
        else:
            print(msg)
            # 打开串口接收定时器，周期为2ms
            # self.timer.start(2)
            ser.write(msg)
    else:
        pass
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
        return None
    if not (num > 0):
        QMessageBox.critical(self, "错误", "串口无回复！")
        return None
    if num > 4:
        if self.dev == '2' or self.dev == "4":
            data = clock.ser.read(num)
        else:
            data = ser.read(num)
        if not (data[0] == 0xaa and data[1] == 0x55):
            QMessageBox.critical(self, "错误", "串口回复包头错误")
            return None
        # if data[4] == 0x01:
        #     QMessageBox.information(self, "提示", "设置成功")
        # elif data[4] == 0x02:
        #     QMessageBox.information(self, "提示", "设置成功")
        # elif data[4] == 0x03:
        #     QMessageBox.information(self, "提示", "设置成功")
        # elif data[4] == 0x04:
        #     if data[5] == 0x00:
        #         QMessageBox.information(self, "提示", "打开成功")
        #     else:
        #         QMessageBox.information(self, "提示", "关闭成功")
        # elif data[4] == 0x05:
        #     tx_soa = data[5]*256+data[6]
        #     tx_dfb = data[7]*256+data[8]
        #     self.lineEdit_soa.setText(str(tx_soa))
        #     self.lineEdit_dfb.setText(str(tx_dfb))
        # elif data[4] == 0x06:
        #     tx_pd = data[5]*256+data[6]
        #     self.lineEdit_pd.setText(str(tx_pd))
        if data[4] == 0xc5:
            QMessageBox.information(self, "提示", "设置成功")
        # elif data[4] == 0xc7:
        #     QMessageBox.information(self, "提示", "设置成功")
        elif data[4] == 0xdd:
            self.spinBox_pulses_dts.setValue(data[14] * int(self.comboBox_plaus_times.currentText()))
        else:
            QMessageBox.critical(self, "错误", "串口回复数据错误")
    else:
        QMessageBox.critical(self, "错误", "串口回复数据错误")
