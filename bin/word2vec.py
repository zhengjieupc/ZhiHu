#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import os,sys,copy,json,re,math,time,copy,random,datetime,types
import gensim
import datetime


class MySentences(object):
    def __init__(self, trainname, testname):
        self.trainname = trainname
        self.testname = testname

    def __iter__(self):
        return iter(prase(self.trainname, self.testname))

def prase(trainname, testname):
    count = 0
    f = open(trainname)
    for line in f:
        try:
            list = json.loads("["+line+"]")
            id,qid1,qid2,question1,question2,is_duplicate = list
            if len(list)!=6:raise IndexError
#            print question1.split()
#            print question2.split()

            yield question1.split()
            yield question2.split()
            count +=1

        except IndexError:
            log_time("index!=6")
            log_time(line)
        except TypeError, e:
            log_time(e)
            log_time(line)
        except Exception,e:
            log_time(e)
            log_time(line)
    f.close()
    print "write count:%d" %(count)

    f = open(testname)
    count = 0
    for line in f:
        try:
            list = json.loads("["+line+"]")
            id,question1,question2 = list
            if len(list)!=3:raise IndexError
#            print question1.split()
#            print question2.split()
            yield question1.split()
            yield question2.split()
            count +=1

        except IndexError:
            log_time("index!=6")
            log_time(line)
        except TypeError, e:
            log_time(e)
            log_time(line)
        except Exception,e:
            log_time(e)
            log_time(line)
    f.close()
    print "write count:%d" %(count)


def log_time(s):
    now = datetime.datetime.now()
    print "[%s][%s.%s][%s]" %(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())), now.second, now.microsecond, s)



if __name__=="__main__":
    train_filename = "./../../data/train.csv"
    test_filename = "./../../data/test.csv"
    
    # 生成词库 list
    wordWarehousFilename = "./../../data/wordWarehous.csv"
    wordWarehous = []
    for line in prase(train_filename, test_filename):
        wordWarehous.extend(line)
    wordWarehous = set(wordWarehous)
    if os.path.exists(wordWarehousFilename):os.remove(wordWarehousFilename)
    fd.open(wordWarehousFilename,'a')
    fd.write(json.dumps(list(wordWarehous)))
    del wordWarehous
    fd.close()

    sentences = MySentences(train_filename, test_filename)
    model = gensim.models.Word2Vec(sentences, min_count=3, size=100)
    model.save('./word2vec.model')
