import requests
import json
import sys
import os
import tqdm

uid = sys.argv[1]
save_dir = sys.argv[2]

headers ={
"authority" : "weibo.com",
"method": "GET",
"path": "/ajax/profile/getImageWall?uid=6089298680&sinceid=0&has_album=true",
"scheme": "https",
"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
"Cache-Control": "no-cache",
"Client-Version": "v2.44.51",
"Cookie": "SCF=AvkV0btqN0V1yiD_X_1ifbwmmksANtnbUp9TuFGRmkiGDaoB-uEC_Tm6SQA9bSOevbSb6okNmua65KHjult4Nvs.; PC_TOKEN=1d4060581a; UOR=,,login.sina.com.cn; wb_view_log=1920*10801; SINAGLOBAL=5830519516109.261.1705583826459; ULV=1705583826464:7:1:1:5830519516109.261.1705583826459:1701508230462; ALF=1708175868; SUB=_2A25IrVSsDeRhGeNI7lAQ9CvJyTiIHXVrw-hkrDV8PUJbkNAGLRGtkW1NSEgwDj5KLvdhHSKAII4EzAf1t2bwZqVL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFaMcGcoDcNnNj6.gDPp6Ow5JpX5KzhUgL.Fo-cSKzpSh-feoB2dJLoI0YLxK-L1K2L1-eLxK-L1K.L1-eLxK-L1K2L1-eLxK-L1K.L1-eLxKML1h.LBo.LxKqL12zL1h.LxKqL1-zLB.et; WBPSESS=x6mAOxU9FMPUL0b--zOh3IZU46gIxsFGxec4jaSOUbDSz8FPXX4HC1tHx4ZxLnuSt6EBu1eQfkEQkyXJCJEwWS1d_FUMxkSfVaUupPA69uJp7dq3x4r1l4Z68ODT5LBuU8lASPty4E-VRmrYF5KiDw==; XSRF-TOKEN=6RtBo8alBT4NzT5oVwydramk",
"Pragma": "no-cache",
"Referer": "https://weibo.com/uncleduobao?tabtype=album",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
"X-Requested-With": "XMLHttpRequest",
"X-Xsrf-Token": "6RtBo8alBT4NzT5oVwydramk"}


def get_pic_url_list(uid):
    '''
    循环请求getImageWall，uid:爬取目标id， 'sinceid':请求起始位置，滚动的下一次请求起始位置可从上一次的返回json的since_id字段中取出。
    Input:
        uid: str 用户id
    Output:
        pic_url_list: 返回的图片url列表
    '''
    pic_url_list = []
    paper_wall = 'https://weibo.com/ajax/profile/getImageWall?uid={}&sinceid=0&has_album=true'.format(uid)
    for i in range(5):
        res = requests.get(paper_wall,headers=headers)
        pic_list = res.json()['data']['list']
        since_id = res.json()['data']['since_id']
        if since_id == '0':
            break
        pic_url_list.extend(['https://wx2.sinaimg.cn/orj360/{}.jpg'.format(pic_info['pid']) for pic_info in pic_list])
        paper_wall = 'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid={since_id}&has_album=true'.format(uid=uid, since_id=since_id)
    return pic_url_list

def download_pic(pic_url, save_dir):
    '''
    爬取一张图片，提取url中的图片id，写到目标文件夹下的id文件中
    Input:
        pic_url: str 图片url
        save_dir: str 目标文件夹
    '''
    res = requests.get(pic_url,headers=headers)
    pic_id = pic_url.split('/')[-1]
    with open(os.path.join(save_dir, pic_id),'wb') as fb:
        fb.write(res.content)

if __name__ == '__main__':
    pic_url_list = get_pic_url_list(uid)
    for pic_url in tqdm.tqdm(pic_url_list):
        download_pic(pic_url, save_dir)