#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 17:39:40 2021

@author: wmm
"""
import os
import pandas as pd
import requests
import xlwt
import time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES=5
import urllib.request
from urllib.request import urlretrieve

## 参考博文https://blog.csdn.net/fangyu723/article/details/122780930
#下载function
def DownloadTif(url):
    try:
        urllib.request.urlretrieve(url)
        print("Downloading")
        #page=urllib.request.urlopen(url)
    except Exception as e:
        print(url+"下载异常："+str(e))
        return

## 参考博文https://blog.51cto.com/u_15200177/2787553
## 建立一个function，自动爬去提取到的PDB结构对应的url，即网页源码里的ID，右键之后选择copy--copy。selector即可见
def get_real_url(url):
    rs=requests.get(url, headers={"Connection":"open"}, verify=False)
    #print(rs.url)
    #return rs.url
    open("/Users/wmm/desktop/"+PDB_ID+".pdb").write(rs.content)




#######################################################################
##打开存有PDB ID 的excel文件，依次提取其中的ID存入list用于之后的爬虫提取
#######################################################################


#从中依次提取库中每一个蛋白对应的PDB_ID
PDB_data=pd.read_excel(r'PDB_ID.xlsx', sheet_name=1)
data_length=len(PDB_data)
PDB_ID=[]
i=0
while i < data_length:
    if isinstance(PDB_data["PDB_ID"][i], str):
        PDB_ID.append(PDB_data["PDB_ID"][i])
    else:
        pass
    i+=1
print("PDB_ID:", PDB_ID)




#######################################################################
##依次提取上文收集的id list中对应的蛋白结构
#######################################################################


n=0
#开始挨个查找
for ID in PDB_ID:
    print("PDB_ID", ID)
    #依次输入搜索的id，获取相应的网页源码
    html=requests.get("https://www.rcsb.org/structure/"+ID, headers={"Connection":"close"}, verify=False)
    #time.sleep(5)
    res=html.text
    #再次封装，利用beautifulsoup包解析获取具体标签内的内容，关键词为html.parser
    bs=BeautifulSoup(res, 'html.parser')
    #利用选择器，读取对应结构的地址url
    tr=bs.select('#DownloadFilesButton > ul > li:nth-child(3) > a')
    print(type(tr))
    print("tr:", tr)
    #把改地址转变成字符串，改编成浏览器常用url格式，再用爬取功能提取
    real_url="https://"+str(tr).split("\"")[1].split("//")[1]
    print("real_url:", real_url)
    ## 显示当前工作路径，即下载之后PDB文件保存的路径
    dir=os.path.abspath('.')
    print("work_path:", dir)
    #get_real_url(real_url)
    #DownloadTif(real_url)
    #以下内容参考https://www.zkxjob.com/534
    rs=requests.get(real_url, headers={"Connection":"close"}, verify=False)
    #print(type(rs))
    open("/Users/wmm/desktop/"+ID+".pdb", "wb").write(rs.content)




