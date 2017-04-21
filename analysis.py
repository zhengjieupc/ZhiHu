#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import os,sys,copy,json,re,math,time,copy,random,datetime,types
import gensim
import datetime
import numpy as np

####统计所有词大概有多少词在word2vec模型中
###将所有词相应的向量放入wordsvecfile：{"word":word_vector}
def wordbook(wordhousefile, modelfile):
   wordvec = {}
   model = gensim.models.Word2Vec.load(modelfile)
   fd = open(wordhousefile)
   count_all = 0
   count_vec = 0
   count_error = 0
   line = fd.readline()
   wordhouse = json.loads(line)
   log_time("begin")
   for word in wordhouse:
      word_count = wordhouse[word]
      if word in (",", "(", ")"): continue
      count_all += 1
      try:
         wordvec.setdefault(word, model[word].tolist())
         count_vec += 1
      except Exception,e:
         log_time(e)
      if re.findall(r"\W", word):
         print word
         count_error += 1
   log_time("end")
   print "the word number of train and test: %d"  %(count_all)
   print "the number of word in word2vec model %d" %(count_vec)
   print "the number of word with not letter or number%d" %(count_error)
   fd.close()
   wordsvecfile = "./../../data/wordsvector.txt"
   if os.path.exists(wordsvecfile): os.remove(wordsvecfile)
   f = open(wordsvecfile, 'a')
   f.write(json.dumps(wordvec))
   f.close

def log_time(s):
   now = datetime.datetime.now()
   print "[%s][%s.%s][%s]" %(time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time())), now.second, now.microsecond, s)

def train_data(filename):
    f = open(filename)
    count = 0
    for line in f:
        line = line.strip().split("\t")
        if line[-1] == "1":
            count += 1
            print line
    print "the numer of label = 1 is %d" %(count)
    f.close()

def senten_len(filename):
    f = open(filename)
    dic = {}
    for line in f:
        line = line.strip().split("\t")
        tmp = [len(json.loads(line[0])), len(json.loads(line[1]))]
        for i in tmp:
            dic.setdefault(i, 0)
            dic[i] += 1
    dic = sorted(dic.iteritems(), key=lambda d:d[0], reverse = False)
    print "len"+","+"count"
    for length, count in dic:
        print "%d,%d" %(length,count)


if __name__=="__main__":
   train_filename = "./../../data/train_lower.csv"
   test_filename = "./../../data/test_lower.csv"
   #词库 list
   wordWarehousFilename = "./../../data/wordWarehous.csv"
   #word2vec模型文件
   modelfilename = "./../../model/word2vec.model"
   ###统计单词个数
   #wordshousedic = wordbook(wordWarehousFilename, modelfilename)
   ###统计训练数据　正负样本情况
   #train_data(train_filename)
   senten_len(test_filename)
