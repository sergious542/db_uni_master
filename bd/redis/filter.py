import redis
import json
import pickle

r = redis.StrictRedis(host='localhost', port=6379, db=1)


def set_filter(session_key, id_category, data):
    d = r.hgetall(session_key)
    # print(d[b'id'])
    d[str(id_category)] = data
    r.hmset(session_key, d)
    r.expire(session_key, 60 * 60 * 24 * 31)
    d = r.hgetall(session_key)
    # print(d)


def get_filter(session_key, id_category):
    try:
        d = (r.hmget(session_key, id_category)[0]).decode('utf-8')
        s = json.dumps(d)

        t = json.loads(s)
        s = t[1:-1].split(',')
        data = {}
        for i in s:
            m = i.split(':')
            data[m[0].split("'")[1].split("'")[-1]] = m[1].split("'")[1].split("'")[-1]
        return data
    except:
        return {}
