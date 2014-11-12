#coding=utf-8
__author__ = 'Administrator'

import requests
from bs4 import BeautifulSoup
import re
import json
import os

DIR = 'D:/music/'
SINGER = '王菲'
START = 0


def getUrl(singer, name):
    return 'http://box.zhangmen.baidu.com/x?op=12&count=1&title=' + name +'$$' + singer + '$$$$';

def download(singer, name):
    url = getUrl(singer, name)
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    encode = soup.find('encode')
    if encode is not None:
        drl1 = encode.contents[0]
        drl1 = drl1[:drl1.rindex('/')]
        drl2 = soup.find('decode').contents[0]
        drl = drl1 + '/' + drl2
        # file_list = re.findall("filename=(\S+)", r.headers['Content-Disposition'])
        # filename = file_list[0][1:-1] if len(file_list) > 0 else name.decode('utf-8').encode('gbk')
        filename = os.path.normcase(DIR + unicode(name, 'utf-8')) + '.mp3'
        if not os.path.isfile(filename):
            print 'downloading:' + filename
            r = requests.get(drl)
            f = open(filename, 'wb')
            f.write(r.content)
            f.close()
    else:
        print 'no result for ' + singer + ' : ' + name



if __name__ == '__main__':
    id_map = {}
    soup = BeautifulSoup(requests.get('http://music.baidu.com/artist').text)
    for singer in soup.find_all("a", href=re.compile("/artist/\d+"), class_=None):
        singer_name = singer.text
        id = singer['href'].split('/')[2]
        id_map[singer_name.encode('utf-8')] = id
    id = id_map[SINGER] if id_map.has_key(SINGER) else None
    payloads = {'start':START, 'ting_uid':id}
    while True:
        json = requests.get('http://music.baidu.com/data/user/getsongs', params=payloads).json()
        soup = BeautifulSoup(json['data']['html'])
        song_list = soup.find_all("a", href=re.compile("/song/"))
        if len(song_list) == 0:
            break
        else:
            payloads['start'] += 20
            for song in song_list:
                download(SINGER, song.text.encode('utf-8'))