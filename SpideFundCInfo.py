# -*- coding: utf-8 -*-

__author__ = "sunmg"

import urllib
import urllib2
import json
import sys
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re
import txtUtils
import Config

reload(sys)
sys.setdefaultencoding('utf-8')


class FundSpide:
    # 初始化
    def __init__(self):
        self.baseUrl = "http://gs.amac.org.cn/amac-infodisc/api/pof/fund"
        self.rand = 0.8975492028985173
        self.size = 20

    # 请求
    def load(self, saveData, page):
        data = {
            'rand': self.rand,
            'page': page,
            'size': self.size
        }

        url = self.baseUrl + "?" + urllib.urlencode(data)
        post_data = "{}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)',
            'Referer': 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/index.html',
            'Content-Type': 'application/json'
        }

        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)
        if saveData == False:
            jdata = json.loads(response.read())
            totalPages = int(jdata['totalPages'])
            self.saveAndLoadMore(totalPages)
        else:
            jdata = json.loads(response.read())
            content = jdata['content']
            print 'now load data ', page
            for con in content:
                local_str_time = datetime.fromtimestamp(con['putOnRecordDate'] / 1000.0).strftime('%Y-%m-%d')
                url = 'http://gs.amac.org.cn/amac-infodisc/res/pof' + con['managerUrl'][2:]
                companyUrl = self.getCompanyUrl(url)
                http = 'http://'
                if http in str(companyUrl):
                    linkUrl = companyUrl
                else:
                    linkUrl = 'http://' + str(companyUrl) + "/"
                none = "None"
                list = (u'无', u'无')
                if none not in linkUrl:
                    list = self.spideConnect(linkUrl)
                if companyUrl == None:
                    companyUrl = '无'
                if list == None:
                    list = (u'无', u'无')
                l1 = list[0]
                if l1 == None:
                    l1 = u'无'
                l2 = list[1]
                if l2 == None:
                    l2 = u'无'
                contents = (con['id'] + " >", con['fundName'] + " >", con['managerName'] + " >", local_str_time + " >",
                            companyUrl + " >", l1 + " >", l2 + '\n')
                # excelUtils.write_to_excel(contents)
                txtUtils.write_to_file(contents)

    # 处理数据，请求和保存至本地
    def saveAndLoadMore(self, totalPages):
        index = 1
        while index < 50:
            count = self.get_infoCount()
            index += 1
            if count >= totalPages:
                break
            else:
                self.load(True, count)
                self.write_count(count + 1)
        print "Please choose Continue or Stop! (C or S)"
        raw = raw_input(': ')
        if raw == 'C':
            self.saveAndLoadMore(totalPages)
        else:
            return

    # 进入公司官方网络地址，获取相应的信息
    def spideConnect(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'UTF-8'
            str = response.text
            soup = BeautifulSoup(str, 'html.parser')
            links = soup.find_all('a')
            for link in links:
                con = link.get_text()
                str = u"联系"
                if str in con:
                    urlm = link.get('href')
                    if urlm == None:
                        urlm = ""
                    baseUrl = self.getUrl(url, urlm)
                    return self.getPhoneNum(baseUrl)
        except requests.RequestException, e:
            if hasattr(e, 'reason'):
                print u"错误原因 Error:", e.reason
                return None

    # 获取联系我们的网址
    def getUrl(self, url, endUrl):
        baseUrl = url
        urls = endUrl.split('/')
        for u in urls:
            if u != None or u != "":
                ul = len(u)
                if ul > 0:
                    if u in url:
                        position = url.find(u)
                        ba = url[:position]
                        if ba.endswith('/'):
                            baseUrl = ba + endUrl
                        else:
                            baseUrl = ba + "/" + endUrl
                    else:
                        if url.endswith('/'):
                            baseUrl = baseUrl + endUrl
                        else:
                            baseUrl = baseUrl + "/" + endUrl
                    return baseUrl

                    # 获取公司官方网络地址

    def getCompanyUrl(self, url):
        response = requests.get(url)
        response.encoding = 'UTF-8'
        str = response.text
        soup = BeautifulSoup(str, "html.parser")
        sf = soup.find(href='javascript:void(0);')
        if sf == None:
            return u'无'
        else:
            return sf.get_text()

    # 获取公司联系方式
    def getPhoneNum(self, url):
        response = requests.get(url)
        response.encoding = 'utf-8'
        str = response.text
        soup = BeautifulSoup(str, 'html.parser')
        regex = re.compile(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}\b", re.I)
        email = soup.find(string=regex)
        phone = re.compile(r"\b\+\d{2}\s+\d{2}\s+(.*)|\(?\d{3}[) -]?\d{8}|\d{11}\b", re.I)
        cellPhone = soup.find(string=phone)
        if cellPhone != None:
            cellPhone = cellPhone.lstrip()
        return (email, cellPhone)

    def get_infoCount(self):
        try:
            with open(Config.COUNT_FILE, 'r') as cf:
                count = cf.read()
                if not count:
                    return 0
                else:
                    return int(count)
        except Exception:
            print u'不存在计数文件，可以从头开始抓取'
            return 0

    def write_count(self, count, file=Config.COUNT_FILE):
        try:
            with open(file, 'w') as f:
                f.write(str(count))
                f.close()
        except TypeError:
            print u'页码写入失败'


if __name__ == '__main__':
    f = FundSpide()
    f.load(False, 0)
