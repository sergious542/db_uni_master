import redis

r = redis.StrictRedis(host='localhost', port=6379, db=1)


def set_value_user(id_user, session_key, role):
    r.hmset(session_key, {"id": id_user, "role": role})
    r.expire(session_key, 60 * 60 * 24 * 31)


def check_user(id_user, session_key):
    try:
        id_u = (r.hmget(session_key, "id")[0]).decode('utf-8')
        if int(id_user) == int(id_u):
            return [True, (r.hmget(session_key, "role")[0]).decode('utf-8')]
        else:
            return [False]
    except:
        return [False]


def get_id_user(session_key):
    return (r.hmget(session_key, "id")[0]).decode('utf-8')


# r.hmset("test",{"r":"e","t":"g"})
# print(r.hmget("test","r"))

# r.delete('id')
#print(r.get('zcgsdgf').decode('utf-8'))
#print(int(r.get('id').decode('utf-8'))+20)
#r.set('id','20')
#print(int(r.get('id').decode('utf-8'))+20)
##for x in list:
 #   print((x))
