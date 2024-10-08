# coding: utf-8
# Author: Roy.Luo
# Version: 1.0

import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import datetime
import json
import logging
from uuid import getnode as get_mac
import platform

class LicenseValidator:
    def __init__(self, license_file='license.key', log_file='validation.log'):
        self.license_file = license_file
        self.log_file = log_file
        self.logger = logging.getLogger('license_validator')

    def generate_key(self, salt):
        password = b"fixed_password"  # 使用固定密码
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password))

    def encrypt_license(self, licenses):
        salt = os.urandom(16)
        key = self.generate_key(salt)
        f = Fernet(key)
        license_data = json.dumps(licenses, ensure_ascii=False).encode('utf-8')
        encrypted_data = f.encrypt(license_data)
        with open(self.license_file, 'wb') as file:
            file.write(salt + encrypted_data)
        self.logger.info(f"已创建许可证，包含 {len(licenses)} 个用户")

    def decrypt_license(self):
        try:
            with open(self.license_file, 'rb') as file:
                file_content = file.read()
            salt = file_content[:16]
            encrypted_data = file_content[16:]
            key = self.generate_key(salt)
            f = Fernet(key)
            decrypted_data = f.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode('utf-8'))
        except FileNotFoundError:
            self.logger.error("许可证文件不存在")
            raise
        except (ValueError, json.JSONDecodeError):
            self.logger.error("许可证文件格式错误")
            raise
        except Exception as e:
            self.logger.error(f"解密许可证时发生未知错误: {str(e)}")
            raise

    def validate_license(self, username):
        try:
            licenses = self.decrypt_license()
            now = datetime.datetime.now()
            current_device = platform.node()  # 获取当前设备名称
            for license in licenses:
                if license['username'] == username:
                    expiry_date = datetime.datetime.fromisoformat(license['expiry_date'])
                    if expiry_date > now:
                        if current_device in license['devices']:
                            self.logger.info(f"许可证验证成功。用户: {username}, 设备: {current_device}, 有效期至: {expiry_date}")
                            return True
                        else:
                            self.logger.warning(f"设备未授权。用户: {username}, 当前设备: {current_device}")
                            return False
                    else:
                        self.logger.warning(f"许可证已过期。用户: {username}, 过期日期: {expiry_date}")
                        return False
            self.logger.warning(f"未找到用户 {username} 的许可证")
            return False
        except Exception as e:
            self.logger.error(f"许可证验证失败: {str(e)}")
            return False

def setup_license_validator(log_file='validation.log'):
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        encoding='utf-8')
    return LicenseValidator(log_file=log_file)