import requests
from requests.exceptions import RequestException
import socket
import threading
import time
import urllib3



exit_flag = False
time_out = 3
check_frequency = 10
user_account = "WOOT"
user_password = "WOOT"
ip_address = "WOOT"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def disconnect():
    ip_address = get_ipaddress()
    url = "https://xha.ouc.edu.cn:802/eportal/portal/mac/unbind?callback=dr1005&user_account=" + user_account + "&wlan_user_mac=000000000000&wlan_user_ip=" + ip_address + "&jsVersion=4.1&v=9233&lang=zh"
    get_request(url)

def generate_url(ip):
    return "https://xha.ouc.edu.cn:802/eportal/portal/login?callback=dr1003&login_method=1&user_account=" + user_account + "&user_password=" + user_password + "&wlan_user_ip=" + ip + "&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1&terminal_type=1&lang=zh-c"

def print_log(message, state):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    print(f"[{state}] " + now + ":  " + message)
    

def get_request(url):
    global exit_flag
    try:
        _ = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=5,
            verify = False
        )
        if not exit_flag:
            if check_network():
                print_log("认证成功！","+")
            else:
                print_log("认证失败，请检查学号密码是否填写正确！","-")
    except RequestException as e:
        print_log(f"请求错误，认证失败：{e}","-")
    
def get_ipaddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def check_network(url="https://www.baidu.com", timeout=3):
    global exit_flag
    maintain = False
    while not exit_flag:
        try:
            _ = requests.get(url, timeout=timeout)
            if not maintain:
                print_log("网络连接正常","+")
            maintain = True
        except RequestException as e:
            maintain = False
            print_log("网络连接异常，正在尝试校园网认证","-")
            request_thread = threading.Thread(target=get_request(url=generate_url(get_ipaddress()))).start()
        time.sleep(check_frequency)

def handle_client(conn, addr):
    global exit_flag
    print_log(f"客户端{addr}已经连接，开始超时计时{time_out}秒", "+")
    start_time = time.time()
    buffer = ""
    while not exit_flag:
        try:
            conn.settimeout(time_out)
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            buffer += data
            if "\n" in buffer or "\r" in buffer:
                line = buffer.strip()
                if line.lower() == "exit":
                    print_log("收到退出命令", "+")
                    exit_flag = True
                    conn.sendall(b"Bye!\n")
                    disconnect()
                else:
                    conn.sendall(b"Unknow command!\n")
                    print_log(f"未知命令:{data}", "-")
                    break
        except socket.timeout as e:
            print_log(f"命令接收超时：{e}", "-")
            conn.sendall(b"Input command timeout\n")
            break
    conn.close()

def handle_client(conn, addr):
    global exit_flag
    print_log(f"客户端{addr}已经连接，开始超时计时{time_out}秒", "+")
    start_time = time.time()
    buffer = ""
    while not exit_flag:
        try:
            conn.settimeout(time_out)
            data = conn.recv(1024).decode()
            if not data:
                break
            buffer += data
            if "\n" in buffer or "\r" in buffer:
                line = buffer.strip()
                if line.lower() == "exit":
                    print_log("收到退出命令", "+")
                    exit_flag = True
                    conn.sendall(b"Bye!\n")
                    disconnect()
                else:
                    conn.sendall(b"Unknow command!\n")
                    print_log(f"未知命令:{line}", "-")
                break
        except socket.timeout as e:
            print_log(f"命令接收超时：{e}", "-")
            conn.sendall(b"Input command timeout\n")
            break
    conn.close()
from datetime import datetime
def remote_control(port=8888):
    global exit_flag
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', port))
    s.listen(5)
    # s.settimeout(1)
    print_log(f"远程端口{port}启动", "+")
    while not exit_flag:
        try:
            conn, addr = s.accept()
            threading.Thread(target=handle_client(conn=conn, addr=addr)).start()
        except socket.timeout as e:
            print_log(f"接收命令超时:{e}", "-")
            continue
    s.close()

    
if __name__ == "__main__":
    threading.Thread(target=check_network).start()
    threading.Thread(target=remote_control).start()
