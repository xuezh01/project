# -*- coding: utf-8 -*-
# @Time    : 2019/7/22 15:48
# @Author  : project
# @File    : 热门视频.py
# @Software: PyCharm


import requests
import json
import urllib.parse
import time

# headers = {
#     "Cookie": "install_id=53112482656; ttreq=1$a4ed279b42b9acb3dee9a3a3c2d645ce99ed786f; odin_tt=38d535495242f853ffdf693ae531a152910b1047bbb3ba5c8e2fa7f3cbd7f6a1ec9f6027fc44ea36c4bd45281487d4a7; sid_guard=d074b1c430eef87a3599e20ef34a5555%7C1543976393%7C5184000%7CSun%2C+03-Feb-2019+02%3A19%3A53+GMT; uid_tt=4e0b25bc326fae6b428afc5826243eeb; sid_tt=d074b1c430eef87a3599e20ef34a5555; sessionid=d074b1c430eef87a3599e20ef34a5555",
#     "Accept-Encoding": "gzip",
#     "X-SS-REQ-TICKET": "1543976807598",
#     "X-Tt-Token": "00d074b1c430eef87a3599e20ef34a5555b97ecb95bff1a3d1a81726386a1adf7a91df6c32bfa121fc10400ffede8df72016",
#     "sdk-version": "1",
#     "X-SS-TC": "0",
#     "User-Agent": "com.ss.android.ugc.aweme/350 (Linux; U; Android 8.0.0; zh_CN; MI 5; Build/OPR1.170623.032; Cronet/58.0.2991.0)"
# }
rticket1 = str(round(int(time.time() * 1000)))
headers = {
    "Connection": "keep-alive",
    "Cookie": "odin_tt=061693cae6d43eb26982cbbb2ca61e4b5db4793dab4a6abcf3f210b2a2b67fbf525d9f1774209d04ff5881a4ef61d94c; sid_guard=8b8654e5d3df5f614e4fa8013991ec90%7C1562929280%7C5184000%7CTue%2C+10-Sep-2019+11%3A01%3A20+GMT; uid_tt=1499f1c7d62ec3409e010597329079f6; sid_tt=8b8654e5d3df5f614e4fa8013991ec90; sessionid=8b8654e5d3df5f614e4fa8013991ec90; install_id=80364985395; ttreq=1$127d238a434b5da5bebb92b1e7df447eaa5a9a87; qh[360]=1",
    "Accept-Encoding": "gzip",
    "X-SS-REQ-TICKET": rticket1,
    "X-Tt-Token": "008b8654e5d3df5f614e4fa8013991ec90b9890d456a8c9aa776366a26dd93a5b1b5f5f46702c123f4fad29eb45113c20b47",
    "sdk-version": "1",
    "X-Gorgon": "03006cc00000e402ff82a76ab99929acfc92ea6d3fdf0c7d32f8",
    "X-Khronos": "1564229036",
    "User-Agent": "com.ss.android.ugc.aweme/730 (Linux; U; Android 7.1.1; zh_CN; OS105; Build/NGI77B; Cronet/58.0.2991.0)"
}


def getHTML(url):
    '''
    get方式获取html
    :param url:
    :return:
    '''
    rsp = requests.get(url, headers=headers)
    return rsp.content.decode('utf-8')
    # return rsp.content.decode(rsp.apparent_encoding, 'ignore')


def postHTML(url):
    '''
    post方式获取html
    :param url:
    :return:
    '''

    rsp = requests.post(url, headers=headers)
    return rsp.content.decode('utf-8')
    # return rsp.content.decode(rsp.apparent_encoding, 'ignore')


def getVideo(key):
    '''
    获取第一个视频连接地址
    :param key:
    :return:
    '''
    # 编译关键词
    key = urllib.parse.quote(key)
    # 拼接关键词搜索接口url
    # hot_search 0普通搜索 1热门搜索 type=1 用户列表
    url = 'https://aweme-hl.snssdk.com/aweme/v1/general/search/single/?keyword=' + key + '&offset=0&count=10&is_pull_refresh=0&hot_search=0&latitude=30.725991&longitude=103.968091&ts=1543984658&js_sdk_version=1.2.2&app_type=normal&manifest_version_code=350&_rticket=1543984657736&ac=wifi&device_id=60155513971&iid=53112482656&os_version=8.0.0&channel=xiaomi&version_code=350&device_type=MI%205&language=zh&uuid=862258031596696&resolution=1080*1920&openudid=8aa8e21fca47053b&update_version_code=3502&app_name=aweme&version_name=3.5.0&os_api=26&device_brand=Xiaomi&ssmix=a&device_platform=android&dpi=480&aid=1128&as=a1e5055072614ce6a74033&cp=5813c65d2e7d0769e1[eIi&mas=01327dcd31044d72007555ed00c3de0b5dcccc0c2cec866ca6c62c'
    # 获取搜索界面并转化为json对象
    jsonObj = json.loads(postHTML(url))
    # 获取data对应v

    metes = jsonObj['data']
    uri = ''
    # 多个视频列表捕获第一个视频地址即刻返回视频uri(视频唯一标识)
    for _ in range(20):
        data = metes[_]['aweme_info']['video']
        if 'download_suffix_logo_addr' in data.keys():
            uri = data['download_suffix_logo_addr']['uri']
            break
            # 拼接视频地址 playwm 有水印地址 play无水印地址

    videoURL = 'https://aweme.snssdk.com/aweme/v1/playwm/?video_id=' + uri + '&line=0'

    print(videoURL)
    # 返回视频地址
    return videoURL


def main():
    '''
    入口函数
    :return:
    '''
    ts = str(time.time())
    # 入口url（热门列表url）
    url = 'https://aweme-hl.snssdk.com/aweme/v1/hot/search/list/?detail_list=1&ts=' + ts + '&js_sdk_version=1.13.10&app_type=normal&os_api=25&device_platform=android&device_type=OS105&iid=72586330332&ssmix=a&manifest_version_code=590&dpi=400&uuid=86795503044051&version_code=590&app_name=aweme&version_name=5.9.0&openudid=c2f22121e41a5d07&device_id=50751127063&resolution=1080*2070&os_version=7.1.1&language=zh&device_brand=SMARTISAN&ac=wifi&update_version_code=5902&aid=1128&channel=smartisan&_rticket=1563784042750&mcc_mnc=46000&as=a1a56733bb86ed03654600&cp=746bd557b3573c37e1QaYe&mas=01b602080bf461332c19a32bfd3e4bc9b80c0c6c2cac6ccc0c26a6'
    # 获取热门列表数据
    print(url)
    html = getHTML(url)
    # 转化为json对象
    jsonObj = json.loads(html)
    # 获取每一个热门数据列表
    word_list = jsonObj['data']['word_list']
    index = 1
    # 循环解析每个热门事件
    for li in word_list:
        try:
            # 关键词
            word = li['word']
            # 热度值
            hot_value = li['hot_value']
            # 排名
            hot_index = index
            videoURL = getVideo(word)
            # videoURL = getVideo('吃鸡搞笑视频')
            index += 1
            print("排名：%d ,关键词: %s ,热度值: %d ,视频下载地址: %s" % (hot_index, word, hot_value, videoURL))
            sev(videoURL, word)

        except Exception as e:
            print(e)
            pass
        finally:
            time.sleep(3)


def sev(url, word):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'}
    response = requests.get(url, headers=headers)
    content = response.content
    name = word + 'mp4'
    with open(name, 'wb') as f:
        f.write(content)
        print('{}：下载成功'.format(word))


if __name__ == '__main__':
    main()

