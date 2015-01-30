#-*-coding:utf8-*-
from __future__ import division
from CWB.CL import Corpus
import PyCQP_interface
import os, re

PyCQP_interface.cMaxRequestProcTime = 240 #This setting is extremely important! The default value is 40, which means the maximum time a user can request is 40 second, but this will not suffice the condition that a user query some high frequency word like '今天' (because usually it takes more than a minute to finish querying).

try:
    from cwm.forms import dbdic
except:
    CHOICE = (
        (u'新聞', (('cna', '中央通訊社'),('asbc', '中研院平衡語料庫'))),
        (u'社會網絡', (('plurk', u'噗浪'), ('ptt', u'批踢踢'))),
        (u'政治法律', (('president', u'總統文告'), ('sunflower', u'太陽花學運'), ('ly', u'立法院公報'))),
        (u'兒童習得', (('tccm', '台灣兒童語言語料庫'), ('textbook', u'國小教科書'))),
        (u'口語言談', (('ntuspk', '台大口語語料庫'),)),
    #    (u'世界中文', (('china', u'中國'), ('hongkong', u'香港'), ('singapore', u'新加坡'))),
        (u'其他', (('copener', 'COPEN user'),)),
    )
    
    DB_CHOICE = []
    for cat, corps in CHOICE:
        for corp in corps:
            DB_CHOICE.append(corp)
    
    
    dbdic = dict(DB_CHOICE)

try:
    from ajilock.lock import Cypher
except:
    import sys
    sys.path.append('/var/www/copens')
    from ajilock.lock import Cypher 
cy = Cypher()
 
class Cqp(object):
    def __init__(self, corpus_name, window_size=8, auth=False):
        self.window_size = window_size
        self.corpus_name = corpus_name
        if self.corpus_name == 'copener':
            if auth == False:
                raise Exception('Not auth!')

    def find(self, token, show_pos=False, rsize=None):
        if isinstance(token, unicode):
            token = token.encode('utf-8')
        else:
            try:
                token.decode('utf-8')
            except:
                raise UnicodeError('Encoding error!')
        self.conclst = []
        registry_dir='/usr/local/share/cwb/registry'
        cqp=PyCQP_interface.CQP(bin='/usr/local/bin/cqp',options='-c -r '+registry_dir)
        cqp.Exec(self.corpus_name.upper()+";")

        if token.startswith('cql:'):
            token = token[4:]
            cqp.Query(token)
        elif token.startswith('ncql:'):
            token = token[5:]
            token = convertCQL(token)
            cqp.Query(token)
        else:
            cqp.Query('[word="%s"];' % token)
        
        _rsize=int(cqp.Exec("size Last;"))
        if rsize == None:
            rsize = _rsize
        else:
            if rsize > _rsize:
                rsize = _rsize

        self.results=cqp.Dump(first=0,last=rsize)
#        os.system('kill -9 $(pidof cqp)')

        cqp.Terminate()
        if self.results == [['']]:
            return 'nores'

        corpus = Corpus(self.corpus_name,registry_dir=registry_dir);
        words = corpus.attribute("word","p")
        
        with open(registry_dir+'/'+self.corpus_name) as f:
            cqpreg = f.read()
#            p_attrs = re.findall('ATTRIBUTE\s(\w+)', cqpreg)
            s_attrs = re.findall('STRUCTURE\s(\w+)', cqpreg)
#            print p_attrs           

        s_attrs_dic = {}
        for attr in s_attrs:
            if attr != 's':
                s_attrs_dic[attr] = corpus.attribute(attr, "s")
            if show_pos == True:
                postags = corpus.attribute("pos","p")
            elif show_pos == False:
                pass
    
        for line in self.results:
            output = dict()
            start = int(line[0])
            end = int(line[1])+1
            
            lw = words[start-self.window_size:start]
            if rsize < self.window_size:
                rw = words[end:end+rsize]
            else:
                rw = words[end:end+self.window_size]
            qw = words[start:end]

            if show_pos == True:
                lp = postags[start-self.window_size:start]
                rp = postags[end:end+self.window_size]
                qp = postags[start:end]             

                left = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(lw, lp)])
                mid = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(qw, qp)])
                right = ' '.join(['%s<span>/%s</span>' % (word, pos) for word, pos in zip(rw, rp)])     

            elif show_pos == False:
                left = ' '.join(['%s' % word for word in lw])
                mid = ' '.join(['%s' % word for word in qw])
                right = ' '.join(['%s' % word for word in rw])     

            metainfo = dict()
            for k in s_attrs_dic.iterkeys():
               metainfo[k] = s_attrs_dic[k].find_pos(start)[-1]
            output['conc'] = (left, mid, right)
            output['corp_name'] = dbdic[self.corpus_name]
            output['metainfo'] = metainfo
            output['qpos'] = cy.encrypt('%s_%s_%s' % (self.corpus_name, start, end))
            self.conclst.append(output)

            #self.conclst.sort(key=lambda x:x['post_time'], reverse=True)
#        os.system('kill -9 $(pidof cqp)')








###############
import re, itertools

def convertCQL(string):
    if not isinstance(string, unicode):
        try:
            string = string.decode('utf8')
        except:
            raise UnicodeError('string must be unicode or utf8')
    if 'x' in string: #\x should be considered
        res = re.split('((?:x){1,})', string)
        res = [[i] if 'x' in i else list(i) for i in res]
        res = itertools.chain.from_iterable(res)
        res = list(res)
        res = possibleCombo(lst=res, spec_char='x')
        output = ''
        for i in res:
            for j in i:
                if j != '':
                    #output += i
                    if 'x' in j:
                        output += j
                    else:
                        output += re.sub('(.*)', '[word="\\1"]', j)
            output += '|'
        output = output.strip('|')+';'
        output = re.sub('x', '[]', output)       
    else:
        output = string
    output = output.encode('utf8')

    return output

def possibleCombo(lst, spec_char):
    combinatorics = itertools.product([True, False], repeat=len(lst) - 1)
    solution = []
    for combination in combinatorics:
        i = 0
        one_such_combination = [lst[i]]
        for slab in combination:
            i += 1
            if not slab: # there is a join
                one_such_combination[-1] += lst[i]
            else:
                one_such_combination += [lst[i]]
        for c in one_such_combination:
            if spec_char in c:
                if len(set(c)) != 1:
                    break
                solution.append(one_such_combination)
    return solution
