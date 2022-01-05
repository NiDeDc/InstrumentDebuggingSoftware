import sys
import config as co

from Ui.mainpage import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIntValidator
from App import fengli as fl
from App import guangxun as gx
from App import gaosi as gs
from App import soa
from App import wave
from App import raman
from App import long
from App import clock
from App.personal import person


class OriginWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(OriginWindow, self).__init__()
        self.index = [0, 1, 2, 3, 4, 5, 6, 7]  # 设定初始选框卡的index数组
        # 当前所选仪表类别
        # 1代表两通道，四通道周界和单通道DAS
        # 2代表四通道DAS
        # 3代表超长距离
        self.dev = co.read_config("SELECT", "dev")
        self.show_all_tab()
        self.personal_page = person()  # 采集卡自定义实例

        # self.timer = QTimer(self)
        # self.timer.timeout.connect(fl.receive_data(self))
        if self.dev == "1":
            self.change_das1()
        elif self.dev == "2":
            self.change_das4()
        elif self.dev == "3":
            self.change_long()
        elif self.dev == "4":
            self.change_ch2()
        else:
            pass

    # 加载页面index为0的页面
    def load_page(self):
        for i in range(len(self.index)):
            if self.index[i] == 0:
                self.init(i)
                self.tabWidget.currentWidget().layout().setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
                break
            else:
                pass

    def init(self, val):
        if val == 0:
            fl.init(self)
            # self.setFixedSize(489, 440)
            self.comboBox_len.setEditable(True)
            font = QFont()
            font.setFamily("华文细黑")
            self.comboBox_len.lineEdit().setFont(font)
            self.comboBox_len.setValidator(QIntValidator(0, 131072))
            self.signal_pulse_change(self.comboBox_pulse_change.currentIndex())
        elif val == 1:
            long.init(self)
            # self.setFixedSize(489, 335)
            # 下拉框变为可编辑
            self.comboBox_len_2.setEditable(True)
            font = QFont()
            font.setFamily("华文细黑")
            self.comboBox_len_2.lineEdit().setFont(font)
            self.comboBox_len_2.setValidator(QIntValidator(0, 131072))
        elif val == 2:
            gx.init(self)
            # self.setFixedSize(350, 350)
        elif val == 3:
            gs.init(self)
            # self.setFixedSize(659, 464)
        elif val == 4:
            raman.init(self)
            # self.setFixedSize(659, 641)
        elif val == 5:
            soa.init(self)
            # self.setFixedSize(659, 464)
        elif val == 6:
            wave.init(self)
            # self.setFixedSize(659, 641)
        elif val == 7:
            clock.init(self)
            # self.setFixedSize(659, 464)
        else:
            pass

    # 页面改变后初始化页面信息
    def change_page(self, val):
        for i in range(len(self.index)):
            if self.index[i] == val:
                self.init(i)
                break

    # 采集卡页面函数
    def serial1(self):
        fl.open_com(self)

    def set_freq(self):
        fl.set_freq(self)

    def start_caijika(self):
        fl.start(self)

    def advance_show(self):
        if self.pushButton_advance.text() == "峰值数据发送⩔":
            self.pushButton_advance.setText("峰值数据发送⩓")
            self.groupBox_advance.show()
            # self.setFixedSize(489, 550)
        else:
            self.pushButton_advance.setText("峰值数据发送⩔")
            self.groupBox_advance.hide()
            # self.setFixedSize(489, 440)

    def send_peak(self):
        fl.send_peak(self)

    def pulse_change(self):
        fl.pulsechange(self)

    def signal_pulse_change(self, index):
        if index == 0:
            self.label_pulse_delay.hide()
            self.spinBox_pulse_delay.hide()
        else:
            self.label_pulse_delay.show()
            self.spinBox_pulse_delay.show()

    def bias_set(self):
        fl.setbias(self)

    # 打开自定义页面
    def personal(self):
        self.personal_page.show()
        person.change_card(self.personal_page, "normal")

    # 长距离页面函数
    def serial_long(self):
        long.open_com(self)

    def setfreq_long(self):
        long.set_freq(self)

    def start_long(self):
        long.start(self)

    def advance_long(self):
        if self.pushButton_advance_2.text() == "峰值数据发送⩔":
            self.pushButton_advance_2.setText("峰值数据发送⩓")
            self.groupBox_advance_2.show()
            # self.setFixedSize(489, 445)
        else:
            self.pushButton_advance_2.setText("峰值数据发送⩔")
            self.groupBox_advance_2.hide()
            # self.setFixedSize(489, 335)

    def send_peak_long(self):
        long.send_peak(self)

    def personal_long(self):
        self.personal_page.show()
        person.change_card(self.personal_page, "long")

    def bias_set_long(self):
        long.setbiaslong(self)

    # 光迅页面函数
    def serial2(self):
        gx.open_com(self)

    def read2(self):
        gx.read_data(self)

    def set2(self):
        gx.set_data(self)

    def change_confirm1(self):
        gx.change_confirm(self)

    # 高思页面函数
    def serial3(self):
        gs.open_com(self)

    def read3(self):
        gs.read_data(self)

    def set3(self):
        gs.set_data(self)

    def change_confirm2(self):
        gs.change_confirm(self)

    # 拉曼放大器页面函数
    def raman_transfer(self):
        raman.transfer_change(self)

    def serial6(self):
        raman.open_com(self)

    def read6_1(self):
        raman.read_data_1(self)

    def read6_2(self):
        raman.read_data_2(self)

    def set6_1(self):
        raman.set_data_1(self)

    def set6_2(self):
        raman.set_data_2(self)

    def attention(self):
        QtWidgets.QMessageBox.information(self, "注意事项", "1.Raman泵浦输出功率较大，注意激光防护！！！\n"
                                                        "2.注意OUT1口连接器端面确保清洁！\n"
                                                        "3.端面清洁的光连接器连接好以后，泵浦电流建议缓慢增加。\n"
                                                        "4.断开光连接器连接前，请将泵浦电流设置为0。")

    # SOA页面函数
    def serial4(self):
        soa.open_com(self)

    def read4_1(self):
        soa.read_datatherm(self)

    # def read4_2(self):
    #     soa.read_datapd(self)

    def read4_2(self):
        soa.read_dts_all(self)

    def setplaus4_dts(self):
        soa.set_plaus_dts(self)

    def set4(self):
        soa.set_dataplaus_tls(self)

    # 波形发送器页面函数
    def serial5(self):
        wave.open_com(self)

    def set5(self):
        wave.send_wave(self)

    def set5_2(self):
        wave.send_amplitude(self)

    def read5(self):
        wave.read_vol(self)

    def set5_3(self):
        wave.set_vol(self)

    def read5_2(self):
        wave.read_amplitude(self)

    def wave_amplitude_change(self, val):
        if val < 26:
            self.label_wave_amplitude.setText(wave.amplitude_dict[val])
        else:
            self.label_wave_amplitude.setText("xx")

    def wave_changer(self):
        wave.changer(self)

    # 同步时钟页面

    def serial7(self):
        clock.open_com(self)

    def set_sameplaus(self):
        clock.setplaus(self)

    def set_sameper(self):
        clock.setper(self)

    def set_samtimeout(self):
        clock.setout(self)

    # 整体页面
    def about(self):
        QtWidgets.QMessageBox.about(self, "关于", "版本号：V2.4\n"
                                                "武汉烽理光电技术有限公司")

    def update_record(self):
        QtWidgets.QMessageBox.about(self, "更新日志", "V1.1更新：新增采集卡通道长度选择功能。\n"
                                                  "V1.2更新：修改高思系列PA读取与设置失败bug。\n"
                                                  "V1.3更新：新增在配置文件中隐藏选项卡功能；增加采集卡通道选择数量；修改原来光脉冲模块的名称。\n"
                                                  "V1.3.1更新：修复隐藏选项卡功能导致选项卡整体index改变从而无法初始化对应页面的bug。\n"
                                                  "V1.4更新：新增采集卡发送10个峰值数据功能：主要用来测试采集卡峰值发送功能,可最多发送4通道；新增拉曼放大器页面，增加部分图标。\n"
                                                  "V1.4.1更新：采集卡配置增加选择通道功能。\n"
                                                  "V1.4.2更新：采集卡峰值数据增加选择个数功能。\n"
                                                  "V1.5更新：采集卡峰值数据发送增加自定义位置功能；增加自定义发送峰值位置功能。\n"
                                                  "V1.6更新：SOA增加DTS读取与设置脉冲功能；修改了通讯错误的描述方式。\n"
                                                  "V1.7更新：修改了峰值发送文件的数据格式。\n"
                                                  "V1.71更新：修复以往版本不影响使用的小bug；修改了软件交互的语言描述；增加4通道DAS发送通道数。\n"
                                                  "V1.8更新：更新波形发生器页面；功能栏增加隐藏恢复选项卡;修改设置SOA最大设置脉宽。\n"
                                                  "V2.0更新：增加针对不同仪表更换不同选项卡功能；增加更换背景图功能；采集卡通道长度下"
                                                  "拉框改为可编辑；更新了SOA脉宽倍率；针对四通道DAS增加同步时钟页面，并将同步时钟的"
                                                  "串口转接功能融入之间的选项卡；增加采集卡单/双脉冲切换功能；禁用了老版SOA功能。\n"
                                                  "V2.1更新：修复新版本拉曼放大器页面槽函数连接错误bug；修改串口通信错误时的描述以及优化软件交互。\n"
                                                  "V2.2测试更新：优化四通道DAS光迅页面切换；修改同步时钟板的单位描述；采集卡增加累加次数参数。\n"
                                                  "V2.2.1更新：增加了同步时钟板的串口回复。\n"
                                                  "V2.2.2更新：增加了PZT的电位幅度可调范围;修改页面布局;自定义页面增加发送延迟时间；"
                                                  "兼容32位操作系统；增加采集卡通道记忆功能；增加超长距离的通道个数。\n"
                                                  "V2.3更新：采集卡和超长距离页面增加偏置电压调节；修改超长距离页面串口记忆功能bug；超长距离增加光迅页面。\n"
                                                  "V2.4更新：增加两通道长距离串口转发;更改拉曼设置电流协议。\n")

    def show_all_tab(self):
        self.setupUi(self)
        self.index = [0, 1, 2, 3, 4, 5, 6, 7]
        self.init(0)
        opt = co.get_hide_sections()
        for i in range(len(opt)):
            co.set_config("HIDE", opt[i], '1')
        self.statusbar.setSizeGripEnabled(False)
        if self.dev == "1":
            dev_str = '两、四通道周界，单通道声波'
        elif self.dev == '2':
            dev_str = '四通道声波(串口转发)'
        elif self.dev == '3':
            dev_str = '超长距离周界'
        elif self.dev == "4":
            dev_str = "两通道长距离声波(串口转发)"
        label = QtWidgets.QLabel("当前仪表:" + dev_str + ' ')
        self.statusbar.addPermanentWidget(label, stretch=0)

    def hide_tab(self):
        cur_tab_index = self.tabWidget.currentIndex()  # 在隐藏条件下当前选项卡的索引
        cur_all_index = self.index.index(cur_tab_index)  # 返回隐藏的选项卡在所有选项卡中的索引
        self.index[cur_all_index] = -1  # 使被隐藏的选项卡在所有index的值为-1
        for i in range(cur_all_index + 1, len(self.index)):  # 当前选项卡隐藏后之后的选项卡index-1
            if self.index[i] != -1:
                self.index[i] -= 1
        print(self.index)
        opt = co.get_hide_sections()
        co.set_config("HIDE", opt[cur_all_index], "0")  # config中HIDE节点中的值当前改为0
        self.tabWidget.removeTab(cur_tab_index)
        for i in range(len(self.index)):
            if self.index[i] == self.tabWidget.currentIndex():
                self.init(i)
                break
            else:
                pass

    # 隐藏配置文件中设置需要隐藏的tab
    def disable_tab(self):
        index = [0, 1, 2, 3, 4, 5, 6, 7]  # 模块隐藏之前各模块对应的实际index
        opt = co.get_hide_sections()
        count = 0  # 对隐藏的选项卡计数，因为每隐藏一个tab，之后的选项卡对应的index就会减1
        for i in range(len(opt)):
            if co.read_config("HIDE", opt[i]) == "0":
                self.tabWidget.removeTab(i - count)
                index[i] = -1
                for j in index[i + 1:]:
                    index[j + count] = j - 1
                count = count + 1
            else:
                pass
        print(index)
        return index  # 返回改变后的index数组

    # 换肤
    def skin_niu(self):
        self.setStyleSheet("background-image: url(:/background/牛.jpg)")

    def skin_blue(self):
        self.setStyleSheet("background-image: url(:/background/bule.jpeg)")

    def skin_color(self):
        self.setStyleSheet("background-image: url(:/background/back1.jpg)")

    def skin_wave(self):
        self.setStyleSheet("background-image: url(:/background/back2.jpeg)")

    def skin_clear(self):
        self.setStyleSheet("background-image: NULL)")

    # 仪表模式切换
    # 两通道、四通道周界、单通道DAS
    def change_das1(self):
        self.dev = '1'
        self.show_all_tab()
        co.set_config("HIDE", "long", "0")
        co.set_config("HIDE", "raman", "0")
        co.set_config("HIDE", "wave", "0")
        co.set_config("HIDE", "clock", "0")
        self.index = self.disable_tab()
        self.load_page()
        co.set_config("SELECT", "dev", '1')
        self.closeEvent(self)

    # 四通道DAS
    def change_das4(self):
        self.dev = '2'
        self.show_all_tab()
        co.set_config("HIDE", "long", "0")
        co.set_config("HIDE", "raman", "0")
        co.set_config("HIDE", 'gaosi', '0')
        self.index = self.disable_tab()
        self.load_page()
        co.set_config("SELECT", "dev", '2')
        self.closeEvent(self)
        self.groupBox_20.hide()
        self.comboBox_chancount.setCurrentIndex(2)

    # 超长距离
    def change_long(self):
        self.dev = '3'
        self.show_all_tab()
        co.set_config("HIDE", "fengli", "0")
        co.set_config("HIDE", "gaosi", "0")
        co.set_config("HIDE", "wave", "0")
        co.set_config("HIDE", "clock", "0")
        self.index = self.disable_tab()
        self.load_page()
        co.set_config("SELECT", "dev", '3')
        self.closeEvent(self)

    # 两通道长距离声波串口转发版
    def change_ch2(self):
        self.dev = "4"
        self.show_all_tab()
        co.set_config("HIDE", "fengli", "0")
        co.set_config("HIDE", "gaosi", "0")
        self.index = self.disable_tab()
        self.load_page()
        co.set_config("SELECT", "dev", '4')
        self.closeEvent(self)

    # def event(self, event):
    #     if event.type == 76:
    #         self.setFixedSize(self.sizeHint())
    #     return self.event(event)

    def closeEvent(self, event):
        fl.ser.close()
        long.ser.close()
        gx.ser.close()
        gs.ser.close()
        soa.ser.close()
        wave.ser.close()
        raman.ser.close()
        clock.ser.close()
        co.create_config()
        self.personal_page.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    StartPage = OriginWindow()
    StartPage.show()  # 显示
    sys.exit(app.exec_())
