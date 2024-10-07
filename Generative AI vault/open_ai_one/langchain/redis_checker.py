import redis
from pprint import pprint

def print_values_with_prefix(redis_host='localhost', redis_port=6363, prefix='stickler_ai:'):
    try:
        # Connect to the Redis server
        r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        
        # Scan for keys with the given prefix
        cursor = 0
        while True:
            cursor, keys = r.scan(cursor=cursor, match=f'{prefix}*')
            for key in keys:
                key_type = r.type(key)
                print(f"key = {key}, type = {key_type}")
                if key_type == 'string':
                    value = r.get(key)
                    pritable_ =f'{key} (string): {value}'
                elif key_type == 'list':
                    value = r.lrange(key, 0, -1)
                    pritable_ =f'{key} (list): {value}'
                    for each in value:
                        pprint(each)
                elif key_type == 'set':
                    value = r.smembers(key)
                    pritable_ =f'{key} (set): {value}'
                elif key_type == 'hash':
                    value = r.hgetall(key)
                    pritable_ =f'{key} (hash): {value}'
                elif key_type == 'zset':
                    value = r.zrange(key, 0, -1, withscores=True)
                    pritable_ =f'{key} (zset): {value}'
                else:
                    pritable_ =f'{key} (unknown type)'
                
                pprint(value)
            
            # Exit the loop if cursor is 0, meaning no more keys to scan
            if cursor == 0:
                break
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print_values_with_prefix(
        redis_host="sti-re-wj228iyrko9d.8ycz0d.0001.euc1.cache.amazonaws.com",
        redis_port=6379
    )
