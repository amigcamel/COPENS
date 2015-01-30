#-*-coding:utf-8-*_
import glob, re, os, nltk
from pymongo import Connection
C = Connection(host='localhost', port=27017)
DB = C['copen_wordlist']

VRT_PATH = "/var/local/LOPEN/corpus/CWB/vrt/"
af = glob.glob(VRT_PATH+'/*.vrt')

ptt_path = os.path.join(VRT_PATH, 'ptt.vrt')
af.remove(ptt_path)

def mk_for_small():
    for f in af:
        with open(f) as ff:
            corp_name = f.split('/')[-1].replace('.vrt', '')
            print 'reading:', f
            data = ff.read().decode('utf-8')
            print 'parsing tokens...'
            toks = re.findall('(.*?)\t.*?\n', data)
            print 'making frequency distribution list...'
            fdist = nltk.FreqDist(toks) 
            cnt = 1
            for tok, occ in fdist.iteritems():
                if occ == 1:
                    break
                freq = fdist.freq(tok)
                punc = True
                if re.match(u'[一-龥]+', tok):
                    punc = False
                print tok, occ, freq, punc
                DB[corp_name].save({'_id':cnt, 'tok':tok, 'occ':occ, 'freq':freq, 'punc':punc})
                cnt += 1
        try: 
            DB['meta'].find({'_id':corp_name}).next()
            DB['meta'].update({'_id':corp_name}, {'$set':{'token_number':fdist.N(), 'type_number':fdist.B(), 'hapax_number':len(fdist.hapaxes())}})
        except StopIteration:
            DB['meta'].save({'_id':corp_name, 'token_number':fdist.N(), 'type_number':fdist.B(), 'hapax_number':len(fdist.hapaxes())})


def mk_for_large():
    fdist = nltk.FreqDist()
    f = open(ptt_path)
    def readptt():
        return f.read(1024000).decode('utf-8', 'ignore')
#    tokcon = []
    cnt = 1
    for piece in iter(readptt, ''):
        toks = re.findall('(.*?)\t.*?\n', piece)
        fdist.update(toks)
#        tokcon += toks
        print cnt
        cnt += 1
    return fdist
