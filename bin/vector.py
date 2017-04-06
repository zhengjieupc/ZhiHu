#!/usr/bin/env python
# -*- encoding:utf-8 -*-

import requests
import os,sys,copy,json,re,math,time,copy,random,datetime,types
import gensim
import datetime
import numpy as np

###将所有词相应的向量放入wordsvecfile：{"word":[index,wordcount,similar_word,word_vector]}
def wordbook(wordhousefile, modelfile, min_count):
   wordsdic = {}
   model = gensim.models.Word2Vec.load(modelfile)
   fd = open(wordhousefile)
   index = 0
   code = 0
   line = fd.readline()
   wordhouse = json.loads(line)
   log_time("begin")
   for word in wordhouse:
      word_count = wordhouse[word]
      index += 1
      if word in wordsdic or word_count == 1: continue
      if wordhouse[word] >= min_count:
         try:
            wordvec = model[word].tolist()
            similar = model.most_similar(word,topn=1)[0][0]
         except Exception,e:
            log_time(e)
            wordvec = np.zeros(100).tolist()
            similar = '0'
      else:
         wordvec = model[word].tolist()
         similar = '0'
      code += 1   
      wordsdic[word] = [index, word_count, similar, wordvec]
   log_time("end")
   print "word number: %d"  %(index)
   print "the number of words count > 1 %d" %(code)
   fd.close()
   wordsvecfile = "./../../data/wordsvector.txt"
   if os.path.exists(wordsvecfile): os.remove(wordsvecfile)
   f = open(wordsvecfile, 'a')
   f.write(json.dumps(wordsdic))
   f.close
   del wordsdic
   #return wordsdic

def prase(simi_file):
   count = 0
   f = open(simi_file)
   for line in f:
       try:
           list = json.loads("["+line+"]")
           id,qid1,qid2,question1,question2,is_duplicate = list
           if len(list)!=6:raise IndexError
           yield question1.split(), question2.split(), is_duplicate
           count += 1
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

def simi_vec(simi_file):
   sentence = prase(simi_file)
   wordsvecfile = "./../../data/wordsvector.txt"
   fd = open(wordsvecfile)
   line = fd.readline()
   wordvecdic = json.loads(line)
   fd.close()
   resultfile = "./../../data/result.txt"
   if os.path.exists(resultfile): os.remove(resultfile)
   for sentence1, sentence2, is_duplicate in sentence:
      simidic = {}
      L1, L2, L12= 0.0, 0.0, 0.0
      for word in sentence1:
         try:
            ###对问题１　每个词向量
            wordlist = wordvecdic[word]
            wordindex = wordlist[0]
            wordvec = wordlist[-1]
            array= np.array(wordvec)
            simidic.setdefault(wordindex,array)
            L1 += array.dot(array)
            ###该词相似词向量
            simiword = wordlist[2]
            simiwordindex = wordvecdic[simiword][0]
            simiwordvec = wordvecdic[simiword][-1]
            array = np.array(simiwordvec)
            simidic.setdefault(simiwordindex,array)
            L1 += array.dot(array)
         except Exception,e:
            log_time(e)
      for word in sentence2:
         try:
            wordlist = wordvecdic[word]
            wordindex = wordlist[0]
            wordvecarray = np.array(wordlist[-1])
            if wordindex in simidic:
               L12 += wordvecarray.dot(simidic[wordindex])
            L2 += wordvecarray.dot(wordvecarray)
            ###相似词
            simiword = wordlist[2]
            simiwordindex = wordvecdic[simiword][0]
            simiwordvecarray = np.array(wordvecdic[simiword][-1])
            if simiwordindex in simidic:
               L12 += simiwordvecarray.dot(simidic[simiwordindex])
            L2 += simiwordvecarray.dot(simiwordvecarray)
         except Exception,e:
            log_time(e)
      simi = L12/(np.sqrt(L1)*np.sqrt(L2))
      f = open(resultfile, 'a')
      try:
         f.write(" ".join(sentence1) + "," + " ".join(sentence2) + "," + is_duplicate + "," + str(simi) + "\n")
      except Exception,e:
         log_time(e)
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
   #modelfilename = "./../../model/word2vec.model"
   #wordshousedic = wordbook(wordWarehousFilename, modelfilename, 4)
   simi_vec(train_filename)
   #model = gensim.models.Word2Vec(sentences, min_count=3, size=100)
   #model.save('./../../model/word2vec.model')
