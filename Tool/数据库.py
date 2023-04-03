from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import sqlite3

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 解析请求参数
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        name = query_params.get('name', ['niming'])[0]

        # 将名字存入数据库
        conn = sqlite3.connect('names.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS names (name TEXT)')
        c.execute('INSERT INTO names (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()

        # 从数据库中查询最新的名字
        conn = sqlite3.connect('names.db')
        c = conn.cursor()
        c.execute('SELECT name FROM names ORDER BY ROWID DESC LIMIT 1')
        row = c.fetchone()
        name = row[0] if row else '无名氏'
        conn.close()

        # 从数据库中查询所有名字
        conn = sqlite3.connect('names.db')
        c = conn.cursor()
        c.execute('SELECT ROWID, name FROM names')
        rows = c.fetchall()
        names = [f"{row[0]}. {row[1]}" for row in rows]
        conn.close()

        # 构造响应
        name_list = '<br>'.join(names)
        message = f"您好，{name}！"
        content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>欢迎页面</title>
        </head>
        <body>
            <h1>{message}</h1>
            <h2>以下是已经访问本网站的用户：</h2>
            <p>{name_list}</p>
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

if __name__ == '__main__':
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, MyHandler)
    print('服务器已启动')
    httpd.serve_forever()
