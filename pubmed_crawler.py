#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 17:07:22 2021

@author: wmm
"""

import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()


#输入搜索文献的关键字
key=input("Please input the keywords:") 
#获取输入关键字之后，返回的网页html文件
html=requests.get("https://pubmed.ncbi.nlm.nih.gov/"+"?term="+key, headers={"Connection":"close"}, verify=False)
#用beautifulsoup解析封装前一步活得的html文件
res=html.text
bs=BeautifulSoup(res,'lxml')
#从html文件中提取搜索结果总数
total_number_of_literature=bs.select('div.results-amount')[0].text
total_number=int(total_number_of_literature.split("r")[0])
#print(total_number)

#pubmed默认每页显示10条结果，总页数为结果总数对10取余
total_page=(total_number//10)+1
#print(total_page)
#每一页的结果，依次读取每一个文章的标题和摘要
with open("literature.txt", "a+") as f:
    for page in range(1, total_page):
        for i in range(0, 10):
            #挨个获取结果页面
            url_current=requests.get("https://pubmed.ncbi.nlm.nih.gov/"+"?term="+key+"&page="+str(page), headers={"Connection":"close"}, verify=False)
            res_current=url_current.text
            #把页面封装/解释（by beasutifulsoup包）
            bs_current=BeautifulSoup(res_current,'lxml')
            #找到想要爬取内容在html文件中的id，用beautifulsoup的select功能读取
            #挨个读取文章的标题
            head_current=bs_current.select('a.docsum-title')[i].text
            #写入存储的txt文件
            f.write(head_current.strip())
            f.write("\n")
            #print(head_current.strip())
            #挨个读取文章的摘要
            abstract_current=bs_current.select('div.full-view-snippet')[i].text
            f.write(abstract_current.strip())
            f.write("\n")
            f.write("\n")
            #print(abstract_current)
            i+=1
        page+=1
f.close()
