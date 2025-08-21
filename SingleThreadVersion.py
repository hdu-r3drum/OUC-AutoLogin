import requests
from requests.exceptions import RequestException
import socket
import time
from datetime import datetime


user_account = "WOOT"
user_password = "WOOT"
ip_address = "WOOT"
url = "https://xha.ouc.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=" + user_account + "&user_password=" + user_password + "&wlan_user_ip=" + ip_address + "&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1&terminal_type=1&lang=zh-c"

def generate_url(ip):
    return "https://xha.ouc.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=" + user_account + "&user_password=" + user_password + "&wlan_user_ip=" + ip + "&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1&terminal_type=1&lang=zh-c"

def print_log(message, state):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{state}] " + now + ":  " + message)
    

def get_request(url, ip):
    
    try:
        response = requests.get(
            url
        )
        print_log("认证成功！","+")
        return response
    except RequestException as e:
        print_log(f"请求错误，认证失败：{e}","-")
        return None
    
def get_ipaddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def check_network(url="https://www.baidu.com", timeout=3):
    try:
        _ = requests.get(url, timeout=timeout)
        print_log("网络连接正常","+")
        return True
    except RequestException as e:
        print_log("网络连接异常，正在尝试校园网认证","-")
        return False


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 8888))
server.listen(5)
server.setblocking(False)

running = True
timeout = 0.1
while running:

    network = check_network()

    if network:
        timeout = 5
    else:
        timeout = 0.1

    while not network:
        if check_network():
            # print_log("网络连接正常","+")
            network = True
            time.sleep(3)
        else:
            # print_log("网络连接异常，正在尝试校园网认证","-")
            print_log("正在尝试连接校园网", "+")
            ip = get_ipaddress()
            url = generate_url(ip)
            get_request(url)
        
    try:
        conn, addr = server.accept()
        data = conn.recv(1024).decode().strip()
        print_log(f"收到来自{addr}:{data}","+")
        # print(f"收到来自{addr}:{data}")

        if data.lower() == "exit":
            print_log("收到结束请求，关闭终端\n","+")
            # print("收到结束请求，关闭终端\n")
            running = False
            conn.sendall(b"Bye!\n")
        else:
            conn.sendall(b"Unknown command\n")

        conn.close()
    except TimeoutError:
        print_log("输入命令时间超时\n","-")
        # print("输入命令时间超时\n")
        conn.sendall(b"Command input timeout\n")
        conn.close()
        pass

    except BlockingIOError:
        pass

    time.sleep(timeout)

server.close()
