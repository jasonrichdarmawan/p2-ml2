# remote_addr: target
captcha_dict = {}

def set(key, value):
    captcha_dict[key] = value
    
def validate(key, value):
    result = captcha_dict.get(key) == value
    captcha_dict.pop(key, None)
    
    return result