import time
import os
from subprocess import Popen
from random import *

# read_group info and available api_keys
f_group = open('group_id.dat', 'r')
f_keys = open('api_keys.txt', 'r')

a = []
b = []
flag = True
for i in f_group:
	if flag:
		a.append(i[:-1])
	else:
		b.append(i[:-1])
	flag = (not flag)
groups = dict(zip(a,b))
print len(groups)

api_keys = []
for i in f_keys:
	if len(i) > 20: api_keys.append(i[:-1])
print len(api_keys)


# distribute tasks (each api_keys for 2 groups)
count = 0
flag = 0
for i in groups.keys():
	j = randint(0, len(api_keys)-1)
#	print (['python','single_collect.py', api_keys[count], i, groups[i], str(flag+1)])
	Popen(['python','single_collect.py', api_keys[j], i, groups[i], str(flag+1)])
	time.sleep(900)
	flag += 1
	if (flag%2 == 1):
		count += 1 	
