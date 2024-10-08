# coding: utf-8
# Author: Roy.Luo
# Version: 1.2

import os
import platform
import socket
import sys
import getpass

def get_username():
    """
    获取当前用户名，兼容Windows和Mac
    """
    return getpass.getuser()

def get_device_name():
    """
    获取设备名称，兼容Windows和Mac
    """
    return platform.node()

def get_ip_address():
    """
    获取IP地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "无法获取IP地址"

def get_system_info():
    """
    获取系统信息，兼容Windows和Mac
    """
    if sys.platform.startswith('win'):
        os_version = platform.version()
    elif sys.platform.startswith('darwin'):
        os_version = platform.mac_ver()[0]
    else:
        os_version = platform.version()

    return {
        "用户名": get_username(),
        "设备名": get_device_name(),
        "IP地址": get_ip_address(),
        "操作系统": platform.system(),
        "操作系统版本": os_version,
        "Python版本": platform.python_version()
    }

if __name__ == "__main__":
    info = get_system_info()
    for key, value in info.items():
        print(f"{key}: {value}")