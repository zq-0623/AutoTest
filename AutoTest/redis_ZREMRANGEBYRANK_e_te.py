#!/usr/bin/python3.7

import sys
import redis
pool = redis.ConnectionPool(host='192.168.251.74', port=6379, db=0)
#pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#pool = redis.ConnectionPool(host='localhost', port=6379, db=0, password='yourPassword')
r = redis.Redis(connection_pool=pool)

count= 0
record = 0
for key in r.scan_iter('*_e'):
    count += 1
    keycount=r.zcard(key)
    if keycount > 4001:
        End_member=r.zcard(key) - 2001
        r.zremrangebyrank(name=key,min=0,max=End_member)
        zremkeycount=r.zcard(key)
        print("{}=>{} -> {}".format(key,keycount,zremkeycount))
#print("keys={}".format(count))

for key in r.scan_iter('*_te'):
    count += 1
    keycount=r.zcard(key)
    if keycount > 4001:
        End_member=r.zcard(key) - 2001
        r.zremrangebyrank(name=key,min=0,max=End_member)
        zremkeycount=r.zcard(key)
        print("{}=>{} -> {}".format(key,keycount,zremkeycount))
#print("keys={}".format(count))

