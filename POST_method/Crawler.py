

import requests
import csv
import pandas as pd
from pandas import DataFrame

## 读入需要处理的数据
df=pd.read_csv("results.csv", sep=',', usecols=['current_sequence'])
print(df)

## 对于新加入的预测的理化性质创建空的dataframe便于之后的存储，以Number of amino acids为例子
df_new=pd.DataFrame(columns=['Number of amino acids'])
print(df_new)

##########################################################
## 开始计算，对于每一个序列，依次计算它们的性质然后存储数据
##########################################################
for sequence in df['current_sequence']:
    print("sequence:", sequence)
    input_sequence=sequence

    ##########################################################
    ## 获取网页文件
    ##########################################################
    # 真正的url，通过网络XHR查看请求的文件找到
    url="https://web.expasy.org/cgi-bin/protparam/protparam"
    # 找到真正的data的输入
    data={"sequence":input_sequence}
    res=requests.post(url, data=data)
    # 查看获取的网页文件，进而找到获取的信息的分布，进行下一步提取
    print("res:", res.text)

    ##########################################################
    ## 获取网页文件之后，从中读取需要的数据
    ##########################################################
    ## 读取第一个参数 Number of amino acids 作为例子
    content=res.text.split("<B")[1].split("</B>")[1]
    print("final:", str(content))

    ##########################################################
    ## 读取的数据存入表单中
    ##########################################################
    df_new=df_new.append({"Number of amino acids": content}, ignore_index=True)

## 把数据合并存成.csv文件
df=pd.concat([df, df_new], axis=1)
df.to_csv('results.csv')