def fact(n):
    if n == 0 or n == 1:
        return 1
    return n*fact(n-1)

def Lq(c, l, m, r):
    num = (l/m)**c*r
    div = fact(c)*(1-r)**2
    
    s = 0
    
    for i in range(c):
        s = s + (l/m)**i/fact(i)
    
    div = div*((l/m)**c/(fact(c)*(1-r)) + s)

    return num/div

def Wq(c, l, m, r):
    return Lq(c, l, m, r)/l

l = 1
m = 0.308
c = 3

print("start")

wq = 5
while wq >= 2:
    c = c + 1
    r = l/(c*m)
    wq = Wq(c,l,m,r)

print("Finished! Solution is:")
print("c="+str(c)+", Wq="+str(wq))
