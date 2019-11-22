def cond_init_key(key, obj, value={}):
    if key not in obj:
        obj[key] = value
