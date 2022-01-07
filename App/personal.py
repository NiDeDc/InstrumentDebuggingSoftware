from Ui.personal import Ui_Dialog
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from App import fengli as fl
from App import long

import time
import os


class person(QtWidgets.QWidget, Ui_Dialog):
    def __init__(self):
        super(person, self).__init__()
        self.setupUi(self)
        self.card_type = "normal"

    def creat_file(self):
        file_name = "peakpos.txt"
        c = 1
        while os.path.exists(file_name):
            file_name = 'peakpos' + str(c) + '.txt'
            c = c + 1
        # if os.path.exists(file_name):
        #     file_name =
        #     f = open(r'peakpos.txt', 'w')
        #     f.truncate(0)
        #     f.close()
        with open(file_name, 'a+', encoding='utf-8') as f:
            start_postion = self.spinBox_start.value()
            space = self.spinBox_space.value()
            num = self.spinBox_num.value()
            if num > 0:
                peakpos = [0] * num
                peakpos[0] = start_postion
                for i in range(0, num):
                    peakpos[i] = peakpos[0] + i * space
                    f.write(str(peakpos[i])+'\n')
            else:
                QMessageBox.critical(self, "错误", "峰值数量不能为0！")

    def change_card(self, card):
        self.card_type = card

    def send(self):
        num = int(self.comboBox_count.currentText())
        file_names = []
        for i in range(0, num):
            filename = QFileDialog.getOpenFileName(self, '打开文件', '', "Text Files(*.txt)")[0]
            print(filename)
            file_names.append(filename)
        if len(file_names) == 0:
            return None
        else:
            try:
                for i in range(0, num):
                    file = open(file_names[i], "r")
                    print(self.card_type)
                    peakpos = file.readlines()
                    peakpos_ary = [x.strip() for x in peakpos]
                    chan = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B]
                    peak_num = len(peakpos_ary)
                    peak_num_byte1 = peak_num >> 24 & 0xff
                    peak_num_byte2 = peak_num >> 16 & 0xff
                    peak_num_byte3 = peak_num >> 8 & 0xff
                    peak_num_byte4 = peak_num & 0xff
                    if self.card_type == "normal":
                        peakpos_bytes = [0] * len(peakpos_ary) * 2
                        print(len(peakpos_bytes))
                        for j in range(len(peakpos_ary)):
                            peakpos_bytes[j * 2] = int(peakpos_ary[j]) >> 8 & 0xff
                            peakpos_bytes[j * 2 + 1] = int(peakpos_ary[j]) & 0xff
                        print(peakpos_bytes)
                        fl.ser.flushInput()
                        data = bytes([0xaa, 0x55, 0x7e, 0x01,
                                      0x00, 0x04,
                                      peak_num_byte1, peak_num_byte2, peak_num_byte3, peak_num_byte4,
                                      chan[i]]) + bytes(peakpos_bytes) + bytes([0x00, 0xFF, 0xFF, 0x00])
                        print(data)
                        fl.ser.write(data)
                        time.sleep(self.spinBox_delay.value()/1000)
                    elif self.card_type == "long":
                        peakpos_bytes = [0] * len(peakpos_ary) * 3
                        print(len(peakpos_bytes))
                        for j in range(len(peakpos_ary)):
                            peakpos_bytes[j * 3] = int(peakpos_ary[j]) >> 16 & 0xff
                            peakpos_bytes[j * 3 + 1] = int(peakpos_ary[j]) >> 8 & 0xff
                            peakpos_bytes[j * 3 + 2] = int(peakpos_ary[j]) & 0xff
                        print(peakpos_bytes)
                        long.ser.flushInput()
                        data = bytes([0xaa, 0x55, 0x7e, 0x01,
                                      0x00, 0x04,
                                      peak_num_byte1, peak_num_byte2, peak_num_byte3, peak_num_byte4,
                                      chan[i]]) + bytes(peakpos_bytes) + bytes([0x00, 0xFF, 0xFF, 0x00])
                        print(data)
                        long.ser.write(data)
                        time.sleep(self.spinBox_delay.value()/1000)
                    else:
                        pass
            except:
                QMessageBox.critical(self, "错误", "文件不存在或文件格式错误")
