import requests
import json
import sys
import os
import tqdm

uid = sys.argv[1]
save_dir = sys.argv[2]

headers ={}

def get_pic_url_list_imagewall(uid):
    '''
    循环请求getImageWall，uid:爬取目标id， 'sinceid':请求起始位置，滚动的下一次请求起始位置可从上一次的返回json的since_id字段中取出。
    Input:
        uid: str 用户id
    Output:
        pic_url_list: 返回的图片url列表
    '''
    pic_url_list = []
    paper_wall = 'https://weibo.com/ajax/profile/getImageWall?uid={}&sinceid=0&has_album=true'.format(uid)
    while True:
        res = requests.get(paper_wall,headers=headers)
        pic_list = res.json()['data']['list']
        since_id = res.json()['data']['since_id']
        if since_id == '0':
            break
        pic_url_list.extend(['https://wx2.sinaimg.cn/orj360/{}.jpg'.format(pic_info['pid']) for pic_info in pic_list])
        paper_wall = 'https://weibo.com/ajax/profile/getImageWall?uid={uid}&sinceid={since_id}&has_album=true'.format(uid=uid, since_id=since_id)
        print('已加载图片{num}张'.format(num=len(pic_url_list)))
    return pic_url_list

def get_pic_url_list_mymblog(uid):
    '''
    循环请求mymblog，uid:爬取目标id， 'sinceid':请求起始位置，滚动的下一次请求起始位置可从上一次的返回json的since_id字段中取出。
    Input:
        uid: str 用户id
    Output:
        pic_url_list: 返回的图片url列表
    '''
    pic_url_list = []
    mymblog = 'https://weibo.com/ajax/statuses/mymblog?uid={}&page=1&feature=0'.format(uid)
    n = 1
    while True:
        n += 1
        res = requests.get(mymblog, headers=headers)
        post_list = res.json()['data']['list']
        since_id = res.json()['data']['since_id']
        if since_id == '':
            break
        for post in post_list:
            if 'title' not in post:
                pic_url_list.extend(['https://wx2.sinaimg.cn/orj360/{}.jpg'.format(pid) for pid in post['pic_ids']])
            elif '好友圈' in post['title']['text']:
                pic_url_list.extend(['https://wx2.sinaimg.cn/orj360/{}.jpg'.format(pid) for pid in post['pic_ids']])
        mymblog = 'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={pageno}&feature=0&since_id={since_id}'.format(uid=uid, pageno=n, since_id=since_id)
        print('已加载图片{num}张'.format(num=len(pic_url_list)))
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
    pic_url_list = get_pic_url_list_mymblog(uid)
    for pic_url in tqdm.tqdm(pic_url_list):
        download_pic(pic_url, save_dir)
