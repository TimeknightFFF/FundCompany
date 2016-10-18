# -*- coding:utf-8 -*-

__author__ = 'sunmg'

import xlwt
import xlrd
from xlutils.copy import copy
import sys
import Config

reload(sys)
sys.setdefaultencoding('utf-8')

#create a excel file
def create_excel(file = Config.EXCEL_FILE):
    book = xlwt.Workbook(encoding='utf-8',style_compression = 0)
    book.add_sheet('sheet1',cell_overwrite_ok = True)
    book.save(file)
    print u'创建excel文件成功'


def repeat_excel(word,file = Config.EXCEL_FILE):
     print u'正在检测',word,u'是否存在与文件中'
     try:
        workbook = xlrd.open_workbook(file)
        sheet = workbook.sheet_by_index(0)
        words = sheet.col_values(0)
        if word in words:
            print u'用户名已存在excel中',word,u'跳过该用户'
            return True
        else:
            print u'用户名在excel中不存在'
            return False
     except IOError, e:
        if 'No such file' in e.strerror:
            print u'匹配重复时未找到该文件',file
            new_excel(file)
            return False
        return False


def write_to_excel(contents,file=Config.EXCEL_FILE):
    print u'正在写入到文件中'
    try:
        rd = xlrd.open_workbook(file)
        sheet = rd.sheets()[0]
        row = sheet.nrows
        wb = copy(rd)
        sheet = wb.get_sheet(0)
        count = 0
        name = contents[0]
        if not repeat_excel(name,file):
            for content in contents:
                sheet.write(row,count,content)
                count = count+1
                wb.save(file)
                print u'已成功写入到文件',file,u'第',row+1,u'行'
            else:
                print u'内容已存在，跳过写入文件'
    except IOError:
        print u'未找到该文件',file
        book = xlwt.Workbook(encoding='utf-8',style_compression=0)
        book.add_sheet('sheet1',cell_overwrite_ok=True)
        book.save(file)
        print u'已成功创建该文件',file
        write_to_excel(contents,file)