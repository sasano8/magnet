class Operator:
    def __xor__(self, other):
        pass

# selector
def k_(key):
    def get_key(x):
        return x[key]
    return get_key

def a_(attr):
    def get_attribute(x):
        return getattr(x, attr)
    return get_attribute

def k_func(key, *args, **kwargs):
    def get_func_return(x):
        func = x[key]
        return func(*args, **kwargs)
    return get_func_return

def a_func(attr, *args, **kwargs):
    def get_func_return(x):
        func = getattr(x, attr)
        return func(*args, **kwargs)
    return get_func_return

# predicate
def eq_(value):
    pass

def ne_(value):
    pass

def lt_(value):
    pass

def le_(value):
    pass

def ge_(value):
    pass

def gt_(value):
    pass

def is_(value):
    pass

def contains_(value):
    pass

def not_(x):
    pass

def and_(x):
    pass

def or_(x):
    pass

def xor_(x):
    pass