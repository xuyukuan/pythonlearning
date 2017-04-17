# linked list in fp way
def cons(x, y):
    return lambda m: m(x, y)

def car(z):
    return z(lambda p,q: p)

def cdr(z):
    return z(lambda p,q: q)
