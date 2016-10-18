# -*- coding:utf-8 -*-

__author__ = 'Sunmg'

import sys
import Config

reload(sys)
sys.setdefaultencoding('utf-8')

def check_info_exit(word, file = Config.SAVE_FILE):
    try:
        with open(Config.SAVE_FILE, 'r') as f:
            lines = f.readlines()
            if lines == None or len(lines) == 0:
                return False
            print 'check info ',word[0]
            for line in lines:
                if word[0] in line:
                    return True
            return False
    except TypeError , e:
        print e.message


def write_to_file(word, file=Config.SAVE_FILE):
    try:
        with open(Config.SAVE_FILE, 'a') as af:
            havInserted = check_info_exit(word)
            if havInserted:
                print u'该数据已在文件中，跳过'
                return
            else:
                print 'write filing word',word[0],word[1]
                for con in word:
                    af.write(con)
    except TypeError, e:
        print e.message



