#coding:utf8
import requests
import re
import os
import pdb
from threading import Thread 
class fetchPic:
    def __init__(self):
        self.header = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}
        self.urls = ['http://txt.rain8.com/txtsc/']
        self.rePicUrl = re.compile('http://i1291.photobucket.com/albums/b548/a317344465/jiaoxiang/[^"]+')
        self.cnt = 0
    def match_pic_url(self,post_url):
        #get the pic url
        req = requests.get(post_url,headers=self.header)
        html = req.content
        pic_list = self.rePicUrl.findall(html)
        return pic_list
    def save_one_pic(self,pic_url):
        #save one picture.
        req = requests.get(pic_url,stream=True)
        image = req.content
        #./download/
        self.cnt+=1
        filename = ''.join(["./download/",str(self.cnt),".jpg"])
        f =  open(filename,'wb')
        f.write(image)
        f.close()
    def start(self):
        for i in range(1,6):
            url = ''.join(["https://www.lightnovel.cn/thread-554480-",str(i),"-1.html"])
            pic_list = self.match_pic_url(url)
            threadpool = []
            threadid = 0
            for pic in pic_list:
                print 'now i am downloading'+pic
                self.save_one_pic(pic)
            print('one page has been downloaded')
A = fetchPic()
A.start()
#A.save_one_pic('http://i1291.photobucket.com/albums/b548/a317344465/jiaoxiang/0b7b3c780a0508227ab799a01a1a597e_zps2f1787c5.jpg')
