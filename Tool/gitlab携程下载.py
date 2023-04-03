import time

import requests
import json
import re
import asyncio
import aiohttp
import aiofiles
import os
from datetime import datetime
import sys

from time import perf_counter
import more_itertools



list=[]
a=""
dtEnd=""
count=1


def progress_bar(finish_tasks_number, tasks_number):

    percentage = round(finish_tasks_number / tasks_number * 100)
    process = "\r[%3s%%]: |%-50s|" % (percentage, '|' *(percentage // 2) )
    print(process, end='', flush=True)


def Getpage(Gitname):
    url = f'https://gitlab.com/users/{Gitname}/projects.json?page=1&skip_namespace=true&skip_namespace=true'
    r = requests.get(url)
    user_dict = json.loads(r.text)
    htnl = user_dict["html"]

    page_t = re.compile(r'<li class="page-item js-pagination-page.*?=true">(?P<page>.*?)</a>', re.S)
    page_len = page_t.finditer(htnl)
    page = page_t.finditer(htnl)


    if more_itertools.ilen(page_len)==0:
        GetPname(f"https://gitlab.com/users/{Gitname}/projects.json?page=1&skip_namespace=true&skip_namespace=true", Gitname)
    else:
        for page in page:
            page_f = page.group("page")

            url_f = f'https://gitlab.com/users/{Gitname}/projects.json?page={page_f}&skip_namespace=true&skip_namespace=true'
            GetPname(url_f, Gitname)
            # print("将要请求的链接：" + url_f)





def GetPname(url_f,Gitname):
    r = requests.get(url_f)
    user_dict1 = json.loads(r.text)
    htnl = user_dict1["html"]

    obj = re.compile(r'<span class.*?<span class="project-name">(?P<name>.*?)</span>', re.S)
    p_name_result = obj.finditer(htnl)

    p_time = re.compile(r'<span class.*?<span class="project-name">(.*?)</span>.*?datetime="(?P<time>.*?)T(.*?) data-toggle="', re.S)
    time_result = p_time.finditer(htnl)
    global list

    for p_name,time_data in zip(p_name_result,time_result):
        p_name1=p_name.group("name")
        time_data1=time_data.group("time")
        url_name = f'https://gitlab.com/{Gitname}/{p_name1}/-/archive/main/{p_name1}-main.zip'
        list.append(f'{url_name}+{time_data1}')
        # print(f'{url_name}+{time_data1}')


def get_time():
    nowtime=datetime.now()
    return nowtime.strftime("%Y-%m-%d")


async def downfile(url):
    new_url=url.split('+')[0]
    tem=url.split('/')[-1]
    name=tem.split('+')[0]
    time_d=tem.split('+')[1]
    new_name=name.replace("-main",f'_{time_d}')

    timeout = aiohttp.ClientTimeout(total=600)  # 将超时时间设置为600秒
    connector = aiohttp.TCPConnector(limit=2)  # 将并发数量降低

    # print(new_name)
    global count
    async with aiohttp.ClientSession(connector=connector,timeout=timeout) as session:
        async with session.get(new_url) as resp:
            async with aiofiles.open(f'{a} {dtEnd}/{new_name}',mode="wb") as f:
                await f.write(await resp.content.read())
    shu= count/len(list)*100
    progress_bar(shu, 100)
    print(f'{count}-{new_name}完毕')
    count += 1



async def main():
    tasks=[]
    for url in list:
        task=asyncio.create_task(downfile(url))
        tasks.append(task)
    await asyncio.wait(tasks)



if __name__ == '__main__':
    a = input("输入gitlab用户名:")
    dtEnd = get_time()
    folder = os.getcwd() + f'\\{a} {dtEnd}'
    if not os.path.exists(folder):
        os.makedirs(folder)
    Getpage(a)
    print(f'获取{a} {len(list)}条项目正在下载........')

    time_start_2 = time.time()
    asyncio.run(main())
    time_end_2 = time.time()

    print(f'携程：全部下载完毕,耗时:{(time_end_2 - time_start_2):.2f}秒')

    os.system("pause")

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())



