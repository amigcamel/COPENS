#-*-coding:utf8-*-
import argparse

parser = argparse.ArgumentParser(description="test")

parser.add_argument('-c', '--corpus', nargs="+", help='specify corpus name')
parser.add_argument('-t', '--token', help="specify query word")
parser.add_argument('-w', '--windowsize', type=int, help='specify window size')
parser.add_argument('-r', '--rsize', type=int, help="maximum query size")
parser.add_argument('-p', '--showpos', type=int, help="show or hide pos")
parser.add_argument('-a', '--auth', type=int, help='specify authentication status')
parser.add_argument('-s', '--samplingnum', type=int, help='specify sampling number')

args = parser.parse_args()

corpus_names = args.corpus
window_size = args.windowsize
auth = args.auth
token = args.token
show_pos = args.showpos
if show_pos == 0:
    show_pos == False
elif show_pos == 1:
    show_pos == True
rsize = args.rsize
if rsize == 0:
    rsize = None

sampling_num = args.samplingnum
if sampling_num == 0:
    sampling_num == None

from cqpapi import Cqp
import json, random

#conclst = []
#for corpus_name in corpus_names:
#    cqp = Cqp(corpus_name=corpus_name, auth=auth, window_size=window_size)
#    cqp.find(token=token, show_pos=show_pos, rsize=rsize)
#    conclst += cqp.conclst
#print json.dumps(cqp.conclst)


conclst = []
for corpus_name in corpus_names:
    cqp = Cqp(corpus_name=corpus_name, auth=auth, window_size=window_size)
    cqp.find(token=token, rsize=rsize, show_pos=show_pos)
    conclst += cqp.conclst
if sampling_num:
    if sampling_num > len(conclst):
        sampling_num = len(conclst)
    conclst = random.sample(conclst, sampling_num)
print json.dumps(conclst)


#from cqpapi import Cqp
#import sys
#
#args =  sys.argv
#if len(args) != 2:
#    raise Exception('This script takes exactly one argument!')
#
#arg = args[1]
#
#cqp = Cqp('asbc')
#cqp.find(u'今天')
#print cqp.conclst

