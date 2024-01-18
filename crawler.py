import requests
import json
import sys
import os
import tqdm

uid = sys.argv[1]
save_dir = sys.argv[2]

headers ={}


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
