#-*-coding:utf-8-*_
from __future__ import division
from collections import Counter
import os, re, math, cPickle

import sys
CUR_PATH = os.path.dirname(os.path.abspath('.'))
sys.path.append(CUR_PATH)
from misc.mongo import mongoDB

# Keyness
#FDIST_PATH = os.path.join(CUR_PATH, "misc/fdist")
FDIST_PATH = '/var/www/copens/misc/fdist'
def load_fdist(corp_name):
    with open(os.path.join(FDIST_PATH, corp_name+'.cpkl')) as f:
        print 'reading:', corp_name
        fdist = cPickle.load(f)
    return fdist

def computeLL(word, ref_corp, tar_corp):
    ref_corp = load_fdist(ref_corp)
    tar_corp = load_fdist(tar_corp)
    tar_sum = sum(tar_corp.values())
    ref_sum = sum(ref_corp.values())
    tar_token_sum = tar_corp[word]
    ref_token_sum = ref_corp.get(word, 0.00000000000000001)
    tar_token_sum = tar_corp.get(word, 0.00000000000000001)

    keyword_sum = tar_token_sum + ref_token_sum
    otherword_sum = tar_sum + ref_sum 
    e1 = float(tar_sum * (keyword_sum / otherword_sum))
    e2 = float(ref_sum * (keyword_sum / otherword_sum))

    if e1 == 0.0:
        e1 = 0.00000000000000001
    elif e1 == 1.0:
        e1 = 0.99999999999999999

    g2 = float(2 * ((tar_token_sum * math.log((tar_token_sum / e1))) + ref_token_sum * math.log((ref_token_sum / e2))))
    
    return g2

def getKeyness(query, ref_corp, database):
    rescon = []
    for b in database:
        try:
            if b[0] != ref_corp:
                res = computeLL('query', ref_corp, b[0])
                rescon.append((b, res))
        except IOError:
            pass # 有一些資料尚未進來！
        except:
            raise
    return rescon


# Thesaurus
from composes.semantic_space.space import Space
from composes.similarity.cos import CosSimilarity
THES_PATH = '/var/www/copens/misc/thesaurus/'
def getThesaurus(word):
    if isinstance(word, unicode):
        word = word.encode('utf-8')
    else:
        try:
            word.decode('utf-8')
        except:
            raise
            
    # find synonyms in chilin
    for line in open(THES_PATH+'chilin-zh-TW.csv'):
        synonyms=line.split()
        if word in synonyms:
            break

    # calculate word similarity
    word_sim_dict={}
    my_space=Space.build(data=THES_PATH+'sm',rows=THES_PATH+'words.rows',cols=THES_PATH+'cols',format='sm')
    for row in open(THES_PATH+'words.rows'):
        word1=row.strip()
        sim=my_space.get_sim(word1,word,CosSimilarity())
        if sim>.3:
            word_sim_dict[word1]=sim

    # rank first those overlapping with chilin synonyms
    word_sim_list=[]
    if word_sim_dict.get(word):
        word_sim_dict.pop(word)
        for key in word_sim_dict.keys():
            if key in synonyms:
                word_sim_dict.pop(key)
                word_sim_list+=[key]

        # sort the rest of words
        d=sorted(word_sim_dict.items(),key=lambda x:x[1],reverse=True)
        word_sim_list+=[word for word,sim in d]

        word_sim_list = word_sim_list[:9]
    return word_sim_list

# Sketch
def getSketch(query, min_logdice=None, min_occ=None):
    res = mongoDB('PTTcollo', 'collo').find({'_id':query}, {'collos':1, 'occ':1})
    try:
        res = res.next()
    except StopIteration:
        return None
    except:
        raise
    if not min_logdice == min_occ == None:
        occ, collos = res['occ'], res['collos'] 
        newdic = {}
        for k, v in collos.iteritems():
            newlst = []
            for vv in v:
                collo_occ, collo_logdice = vv[1], vv[2]
                if collo_occ > min_occ and collo_logdice > min_logdice:
                    newlst.append(vv)
            newdic[k] = newlst
        res = {'occ':occ, 'collos':newdic}
    return res

# Collocation
from collections import OrderedDict
def getCollocation(query, corp_lst, algo_lst, stopword_filter=None):
    '''
    corp_lst should be a list of tuple, e.g., [('asbc', '中央研究院平衡語料庫'), ('plurk', '噗浪'), ...]
    '''
    if not isinstance(query, unicode):
        try:
            query = query.decode('utf8')
        except:
            raise UnicodeError('query should be utf8 or unicode!')
    if not isinstance(corp_lst, list):
        raise TypeError('corp_lst must be a list')
    if not isinstance(algo_lst, list):
        raise TypeError('algo_lst must be a list')
    stopwords = None
    if stopword_filter:
        stopwords = mongoDB('copen_wordlist', 'asbc').find({'punc':{'$eq':False}}, {'_id':0, 'tok':1}).limit(stopword_filter)
        stopwords = set([i['tok'] for i in stopwords])
    resdic = OrderedDict()
    for c, ct in corp_lst:
        for a in algo_lst:
            res = mongoDB('copens_collocation', '%s_%s' % (c, a)).find({}, {'_id':0})
            con = []
            for i in res:
                try:
                    collos = i['collos']
                    if query in collos:
                        if stopword_filter:
                            if not set(collos) & stopwords:
                                con.append(i)
                        else:
                            con.append(i)
                except StopIteration:
                    break
            if not resdic.has_key(ct):
                resdic[ct] = dict()
            resdic[ct][a] = con 

    return resdic, stopwords

# Concordance
#from cqpapi import Cqp
#import random
#def getConcordance(corpus_names, query, window_size=6, show_pos=False, rsize=None, auth=False, sampling_num=None):
#    query = convertCQL(query)
#    if not isinstance(corpus_names, list):
#        raise TypeError('corpus_names must be a list!')
#    conclst = []
#    for corpus_name in corpus_names:
#        cqp = Cqp(corpus_name=corpus_name, auth=auth, window_size=window_size)
#        cqp.find(token=query, rsize=rsize, show_pos=show_pos)
#        conclst += cqp.conclst
#    if sampling_num:
#        if sampling_num > len(conclst):
#            sampling_num = len(conclst)
#        conclst = random.sample(conclst, sampling_num)
#    return conclst 


# wordlist
def getWordlist(database, topnword, punctuations=True, stopwords=True, stopword_level=None):
    if not isinstance(database, list):
        raise TypeError('database must be a list')
    if stopwords == True:
        if stopword_level == None:
            raise Exception('stopword_level should be specify when stopwords == True')
    if stopwords:
        sw = mongoDB('copen_wordlist', 'asbc').find().limit(stopword_level)
        sw = [i['tok'] for i in sw]
    output = dict()
    for dr, dn in database:
        try:
            res = mongoDB('copen_wordlist', dr).find({}, {'_id':0})
            cnt = 0
            con = []
            while cnt < topnword:
                dic = res.next()
                punc = dic['punc']
                if punc == punctuations == True:
                    continue
                if stopwords == True:
                    if dic['tok'] in sw:
                        continue
                con.append(dic)
                cnt += 1
            output[dn] = con
        except StopIteration:
            pass
        except:
            raise
    return output
