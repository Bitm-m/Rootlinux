import re
import os
import socket

import pytz
import datetime
import requests

# 获取本地主机名
host = '0.0.0.0'

# 设置端口号
port = 9999



# 登录地址
LOGIN_URL = "https://my.freenom.com/dologin.php"

# 域名状态地址
DOMAIN_STATUS_URL = "https://my.freenom.com/domains.php?a=renewals"

# 域名续期地址
RENEW_DOMAIN_URL = "https://my.freenom.com/domains.php?submitrenewals=true"

# token 正则
token_ptn = re.compile('name="token" value="(.*?)"', re.I)

# 域名信息正则
domain_info_ptn = re.compile(
  r'<tr><td>(.*?)</td><td>[^<]+</td><td>[^<]+<span class="[^<]+>(\d+?).Days</span>[^&]+&domain=(\d+?)">.*?</tr>',
  re.I,
)

# 登录状态正则
login_status_ptn = re.compile('<a href="logout.php">Logout</a>', re.I)


def SendMesg(message):
  url = f'https://api.telegram.org/bot{TGBOT_TOKEN}/sendMessage'
  headers = {"Content-Type": "application/json"}
  data = {'chat_id': f'{TGBOT_CHAT_ID}', 'text': f'{message}'}
  response = requests.post(url, headers=headers, json=data)
  if response.status_code != 200:
    print(response.text)


def Get_time():
  shanghai = pytz.timezone('Asia/Shanghai')
  shanghai_time = datetime.datetime.now(
    tz=shanghai).strftime("%Y-%m-%d %H:%M:%S")
  return shanghai_time


class FreeNom:

  def __init__(self, username: str, password: str):
    self._u = username
    self._p = password
    self._s = requests.session()
    self._s.headers.update({
      "user-agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/79.0.3945.130 Safari/537.36"
    })

  def _login(self) -> bool:
    self._s.headers.update({
      "content-type": "application/x-www-form-urlencoded",
      "referer": "https://my.freenom.com/clientarea.php",
    })
    r = self._s.post(LOGIN_URL,
                     data={
                       "username": self._u,
                       "password": self._p
                     })
    return r.status_code == 200

  def renew(self) -> str:
    msg = ""
    # login
    if not self._login():
      msg = "login failed"
      print(msg)
      return msg

    # check domain status
    self._s.headers.update(
      {"referer": "https://my.freenom.com/clientarea.php"})
    r = self._s.get(DOMAIN_STATUS_URL)

    # login status check
    if not re.search(login_status_ptn, r.text):
      msg = "get login status failed"
      print(msg)
      return msg

    # page token
    match = re.search(token_ptn, r.text)
    if not match:
      msg = "get page token failed"
      print(msg)
      return msg
    token = match[1]

    # domains
    domains = re.findall(domain_info_ptn, r.text)

    # renew domains
    for domain, days, renewal_id in domains:
      if int(days) < 14:
        self._s.headers.update({
          "referer":
          f"https://my.freenom.com/domains.php?a=renewdomain&domain={renewal_id}",
          "content-type":
          "application/x-www-form-urlencoded",
        })
        r = self._s.post(
          RENEW_DOMAIN_URL,
          data={
            "token": token,
            "renewalid": renewal_id,
            f"renewalperiod[{renewal_id}]": "12M",
            "paymentmethod": "credit",
          },
        )
        result = (f"{domain} 续期成功" if r.text.find("Order Confirmation") != -1
                  else f"{domain} 续期失败")
        # print(result)
        msg += result + "\n"
      result = f"{domain} 还有 {days} 天续期"
      # print(result)
      msg += result + "\n"
    return msg


def main():
  username = os.environ['FN_ID']
  password = os.environ['FN_PW']

  now_time = Get_time()
  freenom = FreeNom(username, password)
  info = freenom.renew()
  global text
  text += f'💸{now_time}💸\n'
  text += info
  SendMesg(text)

  print(now_time)


if __name__ == "__main__":

  # try:
  # except Exception as e:
  #     print("你没有添加任何账户")
  #     exit(1)
  TGBOT_TOKEN = os.environ['TG_TK']
  TGBOT_CHAT_ID = os.environ['TG_ID']
  text = ""
  text += '💖💖Freenoom续期脚本💖💖\n'
  main()
  


  serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # 绑定端口号
  serversocket.bind((host, port))

  # 设置最大连接数，超过后排队
  serversocket.listen(5)
  while True:
    # 建立客户端连接
    clientsocket, addr = serversocket.accept()
    print("连接地址: %s" % str(addr))


    msg = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Hello World</h1></body></html>\r\n"
    clientsocket.send(msg.encode('utf-8'))
    clientsocket.close()
