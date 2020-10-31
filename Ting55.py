# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 13:03:44 2020
@author: fuwen
"""
import requests,re,os,time
from subprocess import call

BookId=3090
#文件下载路径
FilePath = r'D:\有声小说'
#IDM路径
IdmPath = 'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'
Conn=requests.session()
headers = {'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
BookUrl = 'https://m.ting55.com/book/%d'%BookId
BookR = requests.get(BookUrl,headers=headers)
#章节数
BookName = re.findall('<h1>(.*?)</h1>',BookR.text)[0]
BookN = re.findall('<a class="f" href="/book', BookR.text)
print('当前书籍:《%s》'%BookName,'共%d章'%len(BookN))
TingApi = 'https://m.ting55.com/glink'
#已下载文件
AlreadyDown = [FileName.replace('.mp3','',1) for FileName in os.listdir(FilePath)]
#使用IDM下载
def IdmDownLoad(DownloadUrl, Mp3Name):
    call([IdmPath, '/d',DownloadUrl,'/p',FilePath,'/f',Mp3Name,'/n','a'])
# 文件名格式化
def ChangeFileName(filename):
    filename = filename.replace('\\','')
    filename = filename.replace('/','')
    filename = filename.replace('：','')
    filename = filename.replace('*','')
    filename = filename.replace('“','')
    filename = filename.replace('”','')
    filename = filename.replace('<','')
    filename = filename.replace('>','')
    filename = filename.replace('|','')
    filename = filename.replace('?','？')
    filename = filename.replace('（','(')
    filename = filename.replace(' ','')
    filename = filename.replace(chr(65279),'') # UTF-8+BOM
    return filename
#解析文件名、下载路径
def DownLoad(BookId,PageNumber):
    PageUrl = 'https://m.ting55.com/book/%d-%d'%(BookId,PageNumber)
    AudioName = Conn.get(PageUrl,headers=headers)
    AudioName = re.findall('"h1">(.*?)</h1>',AudioName.text)[0]
    AudioName = ChangeFileName(AudioName)
    Resp = Conn.get(PageUrl,headers=headers)
    xt = re.findall('meta name="_c" content="(.*?)"', Resp.text)[0]
    data = {'bookId': BookId,'isPay': 0,'page': 1}
    headers['xt']=xt
    headers['Referer']=PageUrl
    D = Conn.post(TingApi, data=data,headers=headers)
    AudioUrl = D.json()['ourl']
    print('正在下载 %s'%AudioName)
    return AudioName,AudioUrl

for PageNumber in range(len(BookN)):
    PageNumber+=1
    AudioName,AudioUrl = DownLoad(BookId,PageNumber)
    if AudioName in AlreadyDown:
        print('目录已有该文件，跳过下载。')
        continue
    IdmDownLoad(AudioUrl, AudioName+'.mp3')
    time.sleep(10)
