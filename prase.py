#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import os,sys,copy,json,re,math,time,copy,random,datetime,types
import traceback
import datetime



def log_time(s):
    now = datetime.datetime.now()
    print "[%s][%s.%s][%s]" %(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())), now.second, now.microsecond, s)


def prase_train(filename, outfilename):
    f = open(filename)
    
    if os.path.exists(outfilename):os.remove(outfilename)

    fout = open(outfilename, 'a')
    count = 0
    dict = {}
    for line in f:
        try:
            list = json.loads("["+line+"]")
            id,qid1,qid2,question1,question2,is_duplicate = list
            dict[id] = {"qid1":qid1,
                        "qid2":qid2,
                        "question1":question1,
                        "question2":question2,
                        "is_duplicate":is_duplicate}
            if len(list)!=6:raise IndexError
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
    fout.write(json.dumps(dict))
    fout.close()


def prase_test(filename, outfilename):
    f = open(filename)
    
    if os.path.exists(outfilename):os.remove(outfilename)

    fout = open(outfilename, 'a')
    count = 0
    dict = {}
    for line in f:
        try:
            list = json.loads("["+line+"]")
            id,question1,question2 = list
            dict[id] = {"question1":question1,
                        "question2":question2}
            if len(list)!=3:raise IndexError
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
    fout.write(json.dumps(dict))
    fout.close()


if __name__=="__main__":
    train_filename = "./../../data/train.csv"
    outfilename = "./../../data/train.csv.format"
    prase_train(train_filename, outfilename)

    test_filename =  "./../../data/test.csv"
    outfilename = "./../../data/test.csv.format"
    prase_test(test_filename, outfilename)
