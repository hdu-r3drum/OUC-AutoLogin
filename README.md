# OUC-AutoLogin
A tool that frees Ocean University of China students from the hassle of campus network disconnection.

一个基于 **Python 多线程** 实现的校园网自动认证与远程控制工具。  
该程序会自动检测网络连接状态，在掉线时重新向校园网认证服务器发起 GET 请求登录。同时，它提供了一个远程控制端口（默认 8888），可接收远程命令（如 `exit`）来结束程序。

---

## ✨ 功能特性

- **网络状态检测**：定时检测是否可以访问互联网。  
- **自动认证重连**：检测到断网时自动发起校园网登录请求。  
- **日志输出**：所有事件会带时间戳打印，方便排查问题。  
- **远程控制**：通过 TCP 连接到 `8888` 端口，可以远程发送 `exit` 指令来关闭程序。  

---

## ⚙️ 工作原理

1. **网络检测线程**  
   - 定时向指定网址（默认 `https://www.baidu.com`）发起请求。  
   - 如果连接失败，则自动构造校园网认证 URL 并发起登录请求。  

2. **认证线程**  
   - 使用用户账号、密码和本机 IP 生成认证请求 URL。  
   - 使用 `requests` 库发起 GET 请求模拟校园网登录。  

3. **远程控制线程**  
   - 监听本地 `8888` 端口，等待 TCP 连接。  
   - 客户端发送 `exit` 指令后，程序会安全退出。  

---

## 📦 依赖环境

- Python 3.7+
- 第三方库：
  - [requests](https://pypi.org/project/requests/)

安装依赖：

```bash
pip install requests
