import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import re
import pytz
import datetime
import requests

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

text = ""


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


class RequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    # 获取请求参数
    parsed_url = urllib.parse.urlparse(self.path)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    # 处理请求
    name = query_params.get('name', ['匿名用户'])[0]
    if name == '张三':
      message = "您好，张三先生！"
      freenom = FreeNom(username, password)
      info = freenom.renew()
      global text
      text += '💖💖Freenoom续期脚本💖💖\n'
      now_time = Get_time()
      text += f'💸{now_time}💸\n'
      text += info
      SendMesg(text)
      text = ''
    elif name == '李四':
      message = "您好，李四先生！"
    else:
      message = f"您好，{name}！"

    # 构造响应
    content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>欢迎页面</title>
        </head>
        <body>
            <h1>{message}</h1>
        </body>
        </html>
        """
    content_type = 'text/html; charset=utf-8'
    content_length = len(content)

    # 发送响应
    self.send_response(200)
    self.send_header('Content-type', content_type)
    self.send_header('Content-length', content_length)
    self.end_headers()
    self.wfile.write(bytes(content, 'utf-8'))


if __name__ == "__main__":
  username = os.environ['FN_ID']
  password = os.environ['FN_PW']
  TGBOT_TOKEN = os.environ['TG_TK']
  TGBOT_CHAT_ID = os.environ['TG_ID']

  PORT = 8000
  httpd = HTTPServer(("", PORT), RequestHandler)
  print(f"服务器已启动，端口号为 {PORT}")
  httpd.serve_forever()
