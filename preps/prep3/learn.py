class F:
    pass

class G(F):
    pass

class H(F):
    pass


f = F()
g = G()
h = H()
print(isinstance(g, F))
print(isinstance(g, H))
print(type(f) == type(g))
print(type(g) == type(h))
print(isinstance(h, F))
print(isinstance(h, G))
