# coding: utf-8

"""
生成许可证文件

此脚本用于生成包含用户许可信息的加密许可证文件。

使用方法:
1. 运行脚本
2. 按提示输入用户名和过期日期
3. 输入完成后按回车结束输入
4. 脚本将生成加密的许可证文件

功能:
- 允许输入多个用户的许可信息
- 使用 LicenseValidator 类加密许可信息
- 生成包含用户名、过期日期和创建时间的许可证

注意:
- 过期日期格式为 YYYY-MM-DD
- 生成的许可证文件名为 license.key
- 确保 utils/license_validator.py 文件存在且包含 LicenseValidator 类

依赖:
- utils.license_validator
- datetime

作者: Roy.Luo
版本: 1.0
"""

from utils.license_validator import LicenseValidator
import datetime

validator = LicenseValidator()

licenses = []
while True:
    username = input("请输入用户名 (或按回车结束): ")
    if not username:
        break
    expiry_date = input("请输入过期日期 (YYYY-MM-DD): ")
    expiry_date = datetime.datetime.strptime(expiry_date, "%Y-%m-%d")
    
    devices = []
    while True:
        device = input("请输入设备名称 (或按回车结束设备输入): ")
        if not device:
            break
        devices.append(device)
    
    licenses.append({
        'username': username,
        'expiry_date': expiry_date.isoformat(),
        'created_at': datetime.datetime.now().isoformat(),
        'devices': devices
    })

validator.encrypt_license(licenses)
print(f"已生成包含 {len(licenses)} 个用户的许可证")