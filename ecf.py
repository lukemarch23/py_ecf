from random import randrange
from fractions import gcd
from math import log

def prime_sieve(n):
    from math import sqrt;from array import array
    ar = array('B')
    [ar.append(0) for x in xrange(n/16+1)]
    primes = [2,3]
    p=1;sq=int(sqrt(n)+1);i=2
    def setv(n): ar[(n>>3)] |= (1<<(n&7))
    while i<=((n-1)>>1):
        x=(i<<1)+1
        if x<sq and not ar[(i>>3)] & (1<<(i&7)): 
                for k in xrange(x,n/x+1,2):setv((k*x-1)>>1)
        if not ( ar[(i>>3)] & (1<<(i&7)) ) :primes.append((i<<1)+1)
        i+=p;p = 2 if p==1 else 1
    return primes


recommended = [[20,  11000,  86],
[25,  50000,  214],
[30,  250000,     430],
[35,  1000000,   910],
[40,  3000000 ,  2351],
[45,  11000000,  4482],
[50,  43000000,  7557],
[55,  110000000,     17884],
[60,  260000000,     42057],
[65,  850000000,     69471],
[70,  2900000000,   102212],
[75,  7600000000,   188056],
[80,  25000000000,  265557]]

def add(p1, p2, p0, n): # Add two points p1 and p2 given point P0 = P1-P2 modulo n
    x1,z1 = p1; x2,z2 = p2; x0,z0 = p0
    t1, t2 = (x1-z1)*(x2+z2), (x1+z1)*(x2-z2)
    return z0*(t1+t2)**2 % n, x0*(t1-t2)**2 % n
 
def double(p, A, n): # double point p on A modulo n
    x, z = p; An, Ad = A
    t1, t2 = (x+z)**2 % n, (x-z)**2 % n
    t = t1 - t2
    return t1*t2*4*Ad % n, (4*Ad*t2 + t*An)*t % n
 
def multiply(m, p, A, n): # multiply point p by m on curve A modulo n
    if m == 0: return (0, 0)
    elif m == 1: return p
    else:
        q = double(p, A, n)
        if m == 2: return q
        b = 1
        while b < m: b *= 2
        b /= 4
        r = p
        while b:
            if m&b: q, r = double(q, A, n), add(q, r, p, n)
            else:   q, r = add(r, q, p, n), double(r, A, n)
            b /= 2
        return r
from math import ceil,floor
def ilog(x, p): # greatest integer l such that b**l <= x. # TODO: is there a faster way to compute this?  Binsearch, perhaps?
    return int(log(x,p)+1)
 
def ecm(n,verbose = False):   
    l=log(n,10)
    print "ECM",l

    for fd,B1,curves in recommended:
        print fd,"digits",B1,curves
        B2=B1*10
        primes = prime_sieve(B2)
        if verbose:
            print "Trying",fd,B1,B2,curves
        for cv in xrange(curves):
            print fd,"digits", 100.0*cv/curves
            seed = randrange(6, n)
            u, v = (seed**2 - 5) % n, 4*seed % n
            p = u**3 % n
            Q, C = ((v-u)**3*(3*u+v) % n, 4*p*v % n), (p, v**3 % n)
            pi=1
            p=2
            while p <= B1 and pi<len(primes): 
                Q = multiply(p**ilog(B1, p), Q, C, n)
                p=primes[pi]
                pi+=1
            g = gcd(Q[1], n)
            if 1 < g < n: 
                print "Round 1"
                return g
            while p <= B2 and pi<len(primes):
                Q = multiply(p, Q, C, n)
                g *= Q[1]
                if g>n:g %= n
                p=primes[pi]
                pi+=1
            g = gcd(g, n)
            if 1 < g < n: 
                print "Round 2"
                return g
    print "No result found with ecm"
    return None
if __name__ == "__main__":
	print ecm(99877*99991,1)
	from time import time
	t1=time()
	print ecm(523022617466601111760007224100074291200000001,1)
	print time()-t1