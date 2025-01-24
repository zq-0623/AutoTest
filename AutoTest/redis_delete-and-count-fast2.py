# -*- coding: utf-8 -*-

import redis

pool = redis.ConnectionPool(host='114.28.169.95', port=22016, password="SseRedis@123456")
r = redis.Redis(connection_pool=pool)

# patterns = ['*_e', '*_te', '*_ti', '*_t', '*_bs']
patterns = ['*_e', '*_te', '*_ti', '*_t']
key_counts = {}
zlexcount_totals = {}

for pattern in patterns:
    count = 0
    total_zlexcount = 0

    for key in r.scan_iter(pattern):
        count += 1
        key_type = r.type(key).decode('utf-8')

        if key_type == 'zset':
            zset_count = r.zlexcount(key, '-', '+')
            total_zlexcount += zset_count

            if pattern != '*_bs' and zset_count > 20000:
                excess_count = zset_count - 20000
                r.zremrangebyrank(key, 0, excess_count - 1)

    key_counts[pattern] = count
    zlexcount_totals[pattern] = total_zlexcount

for pattern in key_counts:
    count = key_counts[pattern]
    zlexcount = zlexcount_totals[pattern]
    print("Pattern: {}, Keys found: {}, Total zlexcount: {}".format(pattern, count, zlexcount))

total_keys = sum(key_counts.values())
print("Total keys across all patterns: {}".format(total_keys))

