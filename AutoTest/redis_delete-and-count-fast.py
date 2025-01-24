# -*- coding: utf-8 -*-

import redis

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)

#patterns = ['*_e', '*_te', '*_ti', '*_t', '*_bs']
patterns = ['*_e', '*_te', '*_ti', '*_t']
key_counts = {}

for pattern in patterns:
    count = 0

    for key in r.scan_iter(pattern):
        count += 1
        key_type = r.type(key).decode('utf-8')

        if key_type == 'zset':
            zset_count = r.zlexcount(key, '-', '+')

            if pattern != '*_bs' and zset_count > 5000:
                excess_count = zset_count - 5000
                r.zremrangebyrank(key, 0, excess_count - 1)

    key_counts[pattern] = count

for pattern, count in key_counts.items():
    print("Pattern: {}, Keys found: {}".format(pattern, count))

total_keys = sum(key_counts.values())
print("Total keys across all patterns: {}".format(total_keys))

