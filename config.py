import configparser

config = configparser.ConfigParser()


config["FENGLI"] = {
    'port': "COM1",
    'freq': '3000',
    "length": "8000",
    "chCount": "3",
    "add": "4",
    "delay": "50"
}

config["LONG"] = {
    'port': "COM1",
    'freq': '3000',
    "length": "131072",
    "chCount": "3"
}

config['GUANGXUN_PA'] = {
    'port': "COM1"
}

config['GUANGXUN_BA'] = {
    'port': "COM1"
}

config['GAOSI_PA'] = {
    "port": "COM1"
}

config['GAOSI_BA'] = {
    "port": "COM1"
}

config["RAMAN"] = {
    "port": "COM1",
    "transfer": "true"
}

config['SOA'] = {
    'port': "COM1"
}

config['WAVE'] = {
    'port': "COM1"
}

config["CLOCK"] = {
    'port': 'COM1',
    'freq': "1",
    'plaus': "10",
    'timeout': '100'
}

config["POWER"] = {
    'port': 'COM1'
}

config["PCIE"] = {
    'port': 'COM1',
    'freq': '3000',
    "length": "8000",
    "chCount": "3",
    "add": "4",
}

config["HIDE"] = {
    "fengli": "1",
    "long": "1",
    "guangxun": "1",
    "gaosi": "1",
    "raman": "1",
    "tls": "1",
    "wave": "1",
    "clock": "1",
    "power": "1",
    "pcie": "1"
}

# 仪表选择
# 1代表两通道，四通道周界和单通道DAS
# 2代表四通道DAS
# 3代表超长距离
# 4代表两通道周界(串口转发版)
config["SELECT"] = {
    "dev": "1"
}

config.read('config.ini')


def create_config():
    with open('config.ini', 'w') as configfile:
        config.write(configfile)


def set_config(section, option, val):
    config.set(section, option, val)


def read_config(section, option):
    val = config.get(section, option)
    return val


def get_hide_sections():
    opt = config.options("HIDE")
    return opt
