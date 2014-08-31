def compound_interest(m, i, y):
    o = m
    for n in range(1, y+1):
        m = m * (1 + i)
    return m, i, (m - o)/o*1.0

print(compound_interest(1000, 0.05, 2))

def primes(n):
    sieve = [True] * n
    for i in xrange(3, int(n**0.5)+1, 2):
        if sieve[i]:
            sieve[i*i::2*i] = [False] *((n-i*i-1)/(2*i) +1)
    return [2] + [i for i in xrange(3, n, 2) if sieve[i]]


def gcd(n, m):
    # return the greatest common divisor of two numbers
    r = n%m
    if r == 0:
        return m
    return gcd(m, r)

def lcd(n, m):
    return n * m / gcd(n, m)


class Fraction(object):
    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def __add__(self, b):
        numerator = self.numerator * b.denominator  + b.numerator * self.denominator
        denominator = self.denominator * b.denominator
        f = gcd(numerator, denominator)
        return Fraction(numerator/f, denominator/f)

    def __sub__(self, b):
        numerator = self.numerator * b.denominator - b.numerator * self.denominator
        denominator = self.denominator * b.denominator
        f2 = gcd(numerator, denominator)
        return Fraction(numerator/f2, denominator/f2)

    def __mul__(self, b):
        n = self.numerator * b.numerator
        d = self.denominator * b.denominator
        f = gcd(n, d)
        return Fraction(n/f, d/f)

    def __div__(self, b):
        return self * Fraction(b.denominator, b.numerator)

    def __str__(self):
        return '%s/%s' % (self.numerator, self.denominator)

f1 = Fraction(1, 10)
f2 = Fraction(2, 5)
f3 = f1 * f2
print(f1 + f2)
print(f1 - f2)

# common factor
# highest common factor or greatest common divisor GCD
