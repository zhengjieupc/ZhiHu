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


if __name__=="__main__":
   train_filename = "./../../data/train.csv"
   test_filename = "./../../data/test.csv"
   #词库 list
   wordWarehousFilename = "./../../data/wordWarehous.csv"
   #word2vec模型文件
   modelfilename = "./../../model/word2vec.model"
   wordshousedic = wordbook(wordWarehousFilename, modelfilename)
   #simi_vec(train_filename)
   #model = gensim.models.Word2Vec(sentences, min_count=3, size=100)
   #model.save('./../../model/word2vec.model')
