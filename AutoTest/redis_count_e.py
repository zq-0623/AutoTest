# -*- coding: utf-8 -*-

import redis

pool = redis.ConnectionPool(host='114.28.169.95', port=22016, password="SseRedis@123456")
r = redis.Redis(connection_pool=pool)

patterns = ['*_e', '*_te', '*_ti', '*_t']
key_counts = {}
key_sizes = {}
zlexcount_totals = {} 

for pattern in patterns:
    count = 0
    total_size = 0
    total_zlexcount = 0 

    for key in r.scan_iter(pattern):
        count += 1
        key_type = r.type(key).decode('utf-8')

        if key_type == 'string':
            size = r.strlen(key)
            total_size += size
            
        elif key_type == 'zset':
            zset_count = r.zcard(key)
            size = len(key.decode('utf-8')) + (8 * zset_count)
            total_size += size

            zlexcount = r.zlexcount(key, '-', '+')
            total_zlexcount += zlexcount

        elif key_type == 'hash':
            hash_count = r.hlen(key)
            size = len(key.decode('utf-8')) + sum(len(field) + len(value) for field, value in r.hgetall(key).items())
            total_size += size

    key_counts[pattern] = count
    key_sizes[pattern] = total_size
    zlexcount_totals[pattern] = total_zlexcount

for pattern, count in key_counts.items():
    size = key_sizes[pattern]
    zlexcount = zlexcount_totals[pattern]
    print("Pattern: {}, Keys found: {}, Total size: {} bytes, Total zlexcount: {}".format(pattern, count, size, zlexcount))

total_keys = sum(key_counts.values())
total_size = sum(key_sizes.values())
total_zlexcount = sum(zlexcount_totals.values())
print("Total keys across all patterns: {}, Total size: {} bytes, Total zlexcount: {}".format(total_keys, total_size, total_zlexcount))

