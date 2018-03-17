import memcache

cache = memcache.Client(['127.0.0.1:11211'],debug=True)

def set(key,value,timeout=60):   #这个是用来向memcache 写入数据 （默认过期时间是60秒）
    return cache.set(key,value,timeout)

def get(key):                    #这个方法是用来获取memcache中的值
    return cache.get(key)

def delete(key):                 #这个方法用来删除memecache中的值
    return cache.delete(key)




