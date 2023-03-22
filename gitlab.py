import requests
import json
import re
import asyncio
import aiohttp
import aiofiles
import os
from datetime import datetime
import sys
import time



list=[]
a=""
dtEnd=""
count=1


def progress_bar(finish_tasks_number, tasks_number):

    percentage = round(finish_tasks_number / tasks_number * 100)
    process = "\r[%3s%%]: |%-50s|" % (percentage, '|' *(percentage // 2) )
    print(process, end='', flush=True)


def Getpage(Gitname):
    url = f'https://gitlab.com/users/{Gitname}/projects.json?page=2&skip_namespace=true&skip_namespace=true'
    r = requests.get(url)
    user_dict = json.loads(r.text)
    htnl = user_dict["html"]

    page_t = re.compile(r'<li class="page-item js-pagination-page.*?=true">(?P<page>.*?)</a>', re.S)
    page = page_t.finditer(htnl)

    for page in page:
        page_f=page.group("page")
        url_f=f'https://gitlab.com/users/{Gitname}/projects.json?page={page_f}&skip_namespace=true&skip_namespace=true'
        GetPname(url_f,Gitname)
        # print("将要请求的链接：" + url_f)



def GetPname(url_f,Gitname):
    r = requests.get(url_f)
    user_dict1 = json.loads(r.text)
    htnl = user_dict1["html"]
    obj = re.compile(r'<span class.*?<span class="project-name">(?P<name>.*?)</span>', re.S)
    result = obj.finditer(htnl)
    global list

    for Pname in result:
        name=Pname.group("name")
        url_name=f'https://gitlab.com/{Gitname}/{name}/-/archive/main/{name}-main.zip'
        list.append(url_name)



async def downfile(url):
    name=url.rsplit("/",1)[1]
    global count
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            async with aiofiles.open(f'{a} {dtEnd}/{name}',mode="wb") as f:
                await f.write(await resp.content.read())

    # print(f'{name}下载完毕{count}')
    shu= count/len(list)*100
    progress_bar(shu, 100)
    count += 1



async def main():
    tasks=[]
    for url in list:
        task=asyncio.create_task(downfile(url))
        tasks.append(task)
    await asyncio.wait(tasks)


def get_time():
    nowtime=datetime.now()
    return nowtime.strftime("%Y-%m-%d")





if __name__ == '__main__':
    a = input("输入gitlab用户名:")
    dtEnd = get_time()
    folder = os.getcwd() + f'\\{a} {dtEnd}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    Getpage(a)
    print(f'获取{a} {len(list)}条项目正在下载........')
    asyncio.run(main())


