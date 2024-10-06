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
    licenses.append({
        'username': username,
        'expiry_date': expiry_date.isoformat(),
        'created_at': datetime.datetime.now().isoformat()
    })

validator.encrypt_license(licenses)
print(f"已生成包含 {len(licenses)} 个用户的许可证")