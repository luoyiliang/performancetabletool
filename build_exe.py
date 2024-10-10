# coding: utf-8
# Author: Roy.Luo
# Version: 1.1

import os
import shutil
import subprocess
import sys

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        try:
            error_message = error.decode('gbk')  # 首先尝试 GBK 编码
        except UnicodeDecodeError:
            try:
                error_message = error.decode('utf-8')  # 如果 GBK 失败，尝试 UTF-8
            except UnicodeDecodeError:
                error_message = str(error)  # 如果两者都失败，使用字符串表示
        print(f"错误: {error_message}")
        sys.exit(1)
    return output.decode('gbk', errors='replace')  # 使用 GBK 解码输出，忽略无法解码的字符

def main():
    # 确保我们在正确的目录中
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # 创建一个临时目录来存储加密的文件
    if os.path.exists("temp_encrypted"):
        shutil.rmtree("temp_encrypted")
    os.mkdir("temp_encrypted")

    # 使用pyarmor加密代码
    print("正在使用pyarmor加密代码...")
    run_command("pyarmor obfuscate --recursive --output temp_encrypted gui/app.py")

    # 复制其他必要的文件到临时目录
    shutil.copytree("gui", "temp_encrypted/gui", dirs_exist_ok=True)
    shutil.copytree("utils", "temp_encrypted/utils", dirs_exist_ok=True)
    shutil.copy("LICENSE.md", "temp_encrypted/LICENSE.md")

    # 使用PyInstaller创建可执行文件
    print("正在使用PyInstaller创建可执行文件...")
    run_command("pyinstaller --noconfirm --onefile --windowed --add-data \"temp_encrypted/gui;gui\" --add-data \"temp_encrypted/utils;utils\" --add-data \"temp_encrypted/LICENSE.md;.\" temp_encrypted/gui/app.py")

    # 清理临时文件
    print("正在清理临时文件...")
    shutil.rmtree("temp_encrypted")
    if os.path.exists("app.spec"):
        os.remove("app.spec")

    print("打包完成! 可执行文件位于 dist 目录中。")

if __name__ == "__main__":
    main()