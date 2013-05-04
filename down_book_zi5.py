#! /usr/bin/env python
#! encoding:utf-8
# filename:down_book_zi5.py
"""
Copyright 2012 Down_book_zi5
由于最近很多电子书网站被关闭，担心我主要的电子书来源网站也被关闭。
所以写了这个爬虫来自动下载，用于自动下载book.zi5.me上的mobi格式的电子书。
由于Kindle 不支持epub格式，所以网站的上的epub被无视掉了。
@ Python3.3


"""
__author__ = "Sam.huang"
import re
import requests

def remote_down_url(remote_url):
    """
    @remote_url     : 书籍介绍页面
    @regex_file_url : 用于提取书籍页面中电子书下载地址的正则表达式
    @down_url       : 通过re之后得到的完整下载地址
    通过requests.get()下载页面，并用r.text获取页面内容，然后用re匹配下载地址
    """
    regex_file_url = r"/books(.*).mobi"
    down_url_pre = "http://book.zi5.me"
    r = requests.get(remote_url)
    if r.status_code == 200:  #判断网页能否正常访问
        re_file = r.text

        if re.search(regex_file_url,re_file) != None:
            #如果search()的值不为空，即说明能提取到电子书下载地址
            match = re.search(regex_file_url,re_file)
            global down_url
            down_url = str(down_url_pre) + str(match.group())
            print ("DownUrl:",down_url)

        else:
            down_url = "error"
            print ("No Search Down Url.....")
    else:
        print ("ERROR 404!....")


def remote_book_name(remote_url):
    """
    @remote_url     : 书籍介绍页面
    @regex_book_name: 用于提取书籍页面中电子书书名的正则表达式
    @regex_if       : 用于判断页面中是否有书籍
    通过requests.get()下载页面，并用r.text获取页面内容，然后用re匹配书籍名称
    """
    regex_book_name = r'<(.*)子乌书简 &raquo; 书籍 &raquo; (.*)</title>'
    regex_if = r"查无该书"
    r = requests.get(remote_url)
    
    if r.status_code == 200:#判断网页能否正常访问
        re_file = r.text
        
        if re.search(regex_if,re_file) == None:
            #如果search()的值为空，即说明能提取到电子书的书籍名称
            match = re.search(regex_book_name, re_file)
            global book_name
            book_name = match.group(2)+ ".mobi" 
            #使用match.group(2)提取正则表达式里面第二个()的返回值
            print ("BookName:",book_name)
            
        else:
            book_name = "error"
            print ("No Search Book Name.....")
    else:
        print ("ERROR 404!....")


def down_book(down_url,book_name,local_dir):
    """
    @down_dir     : 下载回来的书籍绝对存放路径
    使用write蒋r.content的内容写入到文件
    """
    down_dir = str(local_dir) + str(book_name)
    print (down_dir)
    r = requests.get(down_url)
    with open(down_dir, "wb") as code:
        code.write(r.content)



if __name__ == "__main__":
    url_pre = "http://book.zi5.me/books/detail/"
    local_dir = "D:\\Python\\code\\book_zi5\\book\\"
    for i in range(1, 1251): #目前为止zi5上的页面最大为1251
        url = url_pre + str(i)
        print (url)    
        remote_down_url(url)
        remote_book_name(url)
        if down_url != "error" or book_name != "error":
            down_book(down_url,book_name,local_dir)
        else:
            continue
    else:
        print ("Downing Finish")
  
    




