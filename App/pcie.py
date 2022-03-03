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
    self.spinBox_freq_4.setValue(float(co.read_config("PCIE", "freq")))
    self.comboBox_len_3.setCurrentText(co.read_config("FENGLI", "length"))
    self.comboBox_add_2.setCurrentText(co.read_config("FENGLI", "add"))
    self.comboBox_chancount_3.setCurrentText(co.read_config("FENGLI", "chCount"))
    self.pushButton_advance_3.setText("峰值数据发送⩔")
    self.groupBox_advance_3.hide()


def port_scan(self):
    com_list = list(serial.tools.list_ports.comports())
    self.comboBox_com.clear()
    for i in range(0, len(com_list)):
        por_list = list(com_list[i])
        self.comboBox_com_12.addItem(por_list[0])
    self.comboBox_com_12.setCurrentText(co.read_config("PCIE", "port"))


def set_enabled(self, bol):
    self.comboBox_com_12.setEnabled(not bol)
    self.pushButton_shutdown_2.setEnabled(bol)
    self.pushButton_shutdown_3.setEnabled(bol)
    self.pushButton_shutdown_4.setEnabled(bol)
    self.pushButton_set_7.setEnabled(bol)
    self.pushButton_peadsend_3.setEnabled(bol)
    self.pushButton_personal_3.setEnabled(bol)


def open_com(self):
    if self.pushButton_changer_10.text() == "打开串口":
        ser.port = self.comboBox_com_12.currentText()
        ser.baudrate = 38400
        try:
            ser.open()
            if ser.isOpen():
                set_enabled(self, True)
                self.pushButton_changer_10.setText("关闭串口")
                co.set_config("PCIE", "port", self.comboBox_com_12.currentText())
        except:
            QMessageBox.critical(self, "错误", "打开失败！")
            return None
    else:
        try:
            ser.close()
            self.pushButton_changer_10.setText("打开串口")
            set_enabled(self, False)
        except:
            QMessageBox.critical(self, "错误", "关闭失败！")


def joint_packet(p_type, d_len, data):
    flag = [0xaa, 0x55, 0x7e, 0x01]
    check_num = [0x00, 0xff, 0xff, 0x00]
    end = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    return bytes(flag + p_type + d_len + data + check_num + end)


def set_freq(self):
    p_type = [0x00, 0x02]
    d_len = [0x00, 0x00, 0x00, 0x0e]
    freq = self.spinBox_freq_4.value()
    length = int(self.comboBox_len_3.currentText())
    add = int(self.comboBox_add_2.currentText())
    if add != 0:
        add = add - 1
    ch_count = self.comboBox_chancount_3.currentIndex() + 1
    co.set_config("PCIE", "freq", str(freq))
    co.set_config("PCIE", "length", self.comboBox_len_3.currentText())
    co.set_config("PCIE", "add", self.comboBox_add_2.currentText())
    co.set_config("PCIE", "chCount", self.comboBox_chancount_3.currentText())
    data = [0x22, 0x22,
            freq >> 8 & 0xff, freq & 0xff,
            0x00, 0x0a,
            0x00, ch_count,
            0x00, 0x00, length >> 8 & 0xff, length & 0xff,
            0x00, add & 0xff,
            0x00, 0x03,
            0x00, 0x03]
    w_data = joint_packet(p_type, d_len, data)
    print(w_data)
    ser.flushInput()
    ser.write(w_data)
    receive_data(self, 1)


def set_shutdown(self):
    p_type = [0x00, 0x03]
    d_len = [0x00, 0x00, 0x00, 0x02]
    data = [self.comboBox_pulse_change_2.currentIndex(), 0x00]
    w_data = joint_packet(p_type, d_len, data)
    print(w_data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(w_data)
    receive_data(self, 1)


def set_start(self):
    p_type = [0x00, 0x03]
    d_len = [0x00, 0x00, 0x00, 0x02]
    data = [self.comboBox_pulse_change_2.currentIndex(), 0x01]
    w_data = joint_packet(p_type, d_len, data)
    print(w_data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(w_data)
    receive_data(self, 1)


def set_mode(self):
    p_type = [0x00, 0x08]
    d_len = [0x00, 0x00, 0x00, 0x02]
    data = [0x00, self.comboBox_pulse_change_3.currentIndex()]
    w_data = joint_packet(p_type, d_len, data)
    print(w_data)
    # self.timer.start(2)
    ser.flushInput()
    ser.write(w_data)
    receive_data(self, 1)


def send_peak(self):
    chan = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
    # self.setCursor(Qt.WaitCursor)
    peak_num = self.spinBox_peak_num_3.value()
    peak_bytes = [0] * peak_num * 2
    peak_bytes[1] = 6
    peak_num_byte1 = peak_num >> 24 & 0xff
    peak_num_byte2 = peak_num >> 16 & 0xff
    peak_num_byte3 = peak_num >> 8 & 0xff
    peak_num_byte4 = peak_num & 0xff
    for i in range(3, peak_num * 2, 2):
        peak_bytes[i] = peak_bytes[i - 2] + peak_bytes[i - 3] * (2 ** 8) + 10
        peak_bytes[i - 1] = peak_bytes[i] >> 8 & 0xff
        peak_bytes[i] = peak_bytes[i] & 0xff
    print(peak_bytes)
    p_type = [0x00, 0x04]
    ser.flushInput()
    for i in range(int(self.comboBox_chan_3.currentText())):
        d_len = [peak_num_byte1, peak_num_byte2, peak_num_byte3, peak_num_byte4]
        data = [chan[i]] + peak_bytes
        w_data = joint_packet(p_type, d_len, data)
        print(w_data)
        ser.write(w_data)
        time.sleep(0.5)
        receive_data(self, i)
    # self.setCursor(Qt.ArrowCursor)


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
    if num > 10:
        data = ser.read(num)
        print(data)
        if data[11] == 0x00:
            QMessageBox.critical(self, "错误", "设置失败")
        elif data[11] == 0x01:
            QMessageBox.critical(self, "错误", "设置成功")
        elif data[5] == 0x04:
            if index == int(self.comboBox_chan_3.currentText()) - 1:
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
