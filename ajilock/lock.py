import random, json
from os.path import join, abspath, dirname
from string import digits, ascii_letters, ascii_lowercase

CUR_PATH = dirname(abspath(__file__))

def gentab():
    punctuation = '.:-_'
    cands = digits+ascii_letters+punctuation
    real = digits+ascii_lowercase
    cor = random.sample(cands, len(real))
    real_dic = dict(zip(real, cor))
    dic_rev = dict()
    for k, v in real_dic.iteritems():
        dic_rev[v] = k

    fake = list(set(cands) - set(cor))
    jointer = random.sample(fake, 10)
    fake = list(set(fake) - set(jointer))

    for i in fake:
        dic_rev[i] = ''
    for i in jointer:
        dic_rev[i] = ' '

    with open('lock.json', 'w') as lf, open('unlock.json', 'w') as uf, open('fake.json', 'w') as ff, open('jointer.json', 'w') as jf:
        json.dump(real_dic, lf)
        json.dump(dic_rev, uf)
        json.dump(fake, ff)
        json.dump(jointer, jf)


class Cypher(object):
    def __init__(self, slen=32):
        self.slen = slen

        with open(join(CUR_PATH, 'lock.json')) as lf, open(join(CUR_PATH, 'unlock.json')) as uf, open(join(CUR_PATH, 'fake.json')) as ff, open(join(CUR_PATH, 'jointer.json')) as jf:
            self.lock = json.load(lf)
            self.unlock = json.load(uf)
            self.fake = json.load(ff)
            self.jointer = json.load(jf)

    def encrypt(self, string):
        string = [random.choice(self.jointer) if s == '_' else self.lock[s] for s in string]
        str_len = len(string)
        mask_len = self.slen - str_len
        real_pos = random.sample(range(self.slen), str_len)
        real_pos.sort()
        mask = [random.choice(self.fake) for i in range(mask_len)]
        for i, j in zip(string, real_pos):
            mask.insert(j, i)
        output = ''.join(mask)
        return output

    def decrypt(self, string):
        output = ''.join(self.unlock[i] for i in string)
        print output
        output = output.split(' ')
        return output
