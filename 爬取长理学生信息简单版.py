#@-*- codeing = utf-8 -*-
#@Time : 2020/2/28 20:19
#@Author : 黄春林
#@File : code1.py
#@Software: PyCharm

import requests
import re
from bs4 import BeautifulSoup
import xlwt
find1 = re.compile(r'<div style="min-width: 35px">(\d*)</div></td>')
find2 = re.compile(r'</div></td><td title="(.*?)">')
def main():
    url="http://xk.csust.edu.cn/common/xs0101_select.jsp?pageSize=25157"
    askURL("http://xk.csust.edu.cn/jsxsd/framework/xsMain.jsp")
    #askURL("http://xk.csust.edu.cn/jiaowu/pkgl/llsykb/llsykb_find_xx04.jsp4") # fixed by LooyeaGee at 202008091010
    #直接访问需要账户手动点一下在各类课表查询那里，不然要先访问这里，先决条件。
    #爬取网页
    datalist=getdata(url)
    savepath="长理学生信息.xls"
    saveData(datalist,savepath)
def askURL(url):
    head={#模拟浏览器头部信息，向服务器发送信息
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Cookie": "JSESSIONID=66F8D54A95D0DFC7F543E8C90EEFD87B; _ga=GA1.3.223820084.1582280368; JSESSIONID=A5A47B6F64C01F00A4A2F5017810971F",
    }

    session=requests.Session()
    html=session.get(url,headers=head)
    # print(html)
    # print(html.content)
    return html
def getdata(url):
    datalist = []

    html=askURL(url)
    soup = BeautifulSoup(html.content, "html.parser")

    for item in soup.find_all('tr',style="cursor:pointer;"):

        item = str(item)
        # print(item)
        if re.findall(find2,item):
            f2=re.findall(find2,item)
            datalist.append(f2)
    print(datalist)
    return datalist
def saveData(datalist,savepath):
    print("save....")
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)  #创建workbook对象
    sheet = book.add_sheet('长沙理工大学学生信息',cell_overwrite_ok=True)    #创建工作表
    col = ("学院","专业","年级","班级","学号","姓名","性别")
    for i in range(0,7):
        sheet.write(0,i,col[i]) #列名
    for i in range(0,len(datalist)):
        print("第%d条" %(i+1))
        data = datalist[i]
        for j in range(0,len(data)):
            sheet.write(i+1,j,data[j])      #数据


    book.save(savepath)       #保存


if __name__=="__main__":
    main()
    print("爬取完毕")
