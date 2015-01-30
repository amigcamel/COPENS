#-*-coding:utf-8-*_
import glob, re, os, nltk, cPickle

VRT_PATH = "/var/local/LOPEN/corpus/CWB/vrt/"
af = glob.glob(VRT_PATH+'/*.vrt')

ptt_path = os.path.join(VRT_PATH, 'ptt.vrt')
af.remove(ptt_path)

for f in af:
    with open(f) as ff:
        corp_name = f.split('/')[-1].replace('.vrt', '')
        print 'reading:', f
        data = ff.read().decode('utf-8')
        print 'parsing tokens...'
        toks = re.findall('(.*?)\t.*?\n', data)
        print 'making frequency distribution list...'
        fdist = nltk.FreqDist(toks)
        with open(corp_name+'.cpkl', 'wb') as f:
            cPickle.dump(fdist, f)
        print 'DONE'
