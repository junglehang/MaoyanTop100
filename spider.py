import requests
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool

def get_one_page(url,headers):
    '''
    获取网页html内容并返回
    '''
    try:
        # 获取网页html内容
        response = requests.get(url,headers=headers)
        # 通过状态码判断是否获取成功
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    """
    以生成器方式返回一个格式化字典
    :param html:
    :return:
    """
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         +'.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        yield {
            "index":item[0],
            "image": item[1],
            "title": item[2],
            "actor": item[3].strip()[3:],
            "time": item[4].strip()[4:],
            "source": item[5]+item[6]
        }

def write_to_file(content):
    """
    以json格式写入文件
    :param content:
    :return:
    """
    with open("maoyan.txt","a",encoding="utf-8") as f:
        f.write(json.dumps(content,ensure_ascii=False)+"\n")
        f.close()

def main(offset):
    url = "http://maoyan.com/board/4?offset={0}".format(str(offset))
    #加上请求头才可以请求成功
    headers = {"User-Agent":"Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"}
    html = get_one_page(url,headers)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    #设置进程池提高爬取速度
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])