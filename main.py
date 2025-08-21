import matplotlib.pyplot as plt
import sys
import math

X = 10
Y = 10

RANGE_X = 50
RANGE_Y = 50

PRECISION = 10

DEPTH = 100

#t = "normal"
#args = {}

t2 = "ab"
args2 = {"a": 0.8, "b": 0.8} # Argumentos alfa-beta

#t = "ar"
#args = {"a": 0.7, "r": 0.5}

#t = "ar2"
#args = {"a": 0.8, "r1": 0.5, "r2": 0.8}

t = "asin"
args = {"a": 0.8}

class Cost:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def dominates(self, other):
        return self.c1 < other.c1 and self.c2 < other.c2
    
    def weakly_dominates(self, other):
        return self.c1 <= other.c1 and self.c2 <= other.c2

def ab_transform(a, b, x, y):
    return ((a*x + (1-a)*y), ((1-b)*x + b*y))

def ar_transform(a, r, x, y):
    xr, yr = (x**r, y**r)
    return ((a*xr + (1-a)*yr), ((1-a)*xr + a*yr))

def ar2_transform(a, r1, r2, x, y):
    xr, yr = (x**r1, y**r2)
    return ((a*xr + (1-a)*yr), ((1-a)*xr + a*yr))

def asin_transform(a, x, y):
    xs, ys = (x + math.sin(x), y + math.sin(y))
    return ((a*xs + (1-a)*ys), ((1-a)*xs + a*ys))

def transform(t: str, args: list, x, y):
    match t:
        case "ab":
            return ab_transform(args["a"], args["b"], x, y)
        case "ar":
            return ar_transform(args["a"], args["r"], x, y)
        case "ar2":
            return ar2_transform(args["a"], args["r1"], args["r2"], x, y)
        case "asin":
            return asin_transform(args["a"], x, y)
        case _:
            return (x, y)

def binary_search_x(base: Cost, t, args: list, x: float, low: float, high: float, depth: int):
    mid = (low + high)/2
    if depth == 0:
        return mid
    
    d1, d2 = transform(t, args, x, mid)
    point = Cost(d1, d2)
    if base.weakly_dominates(point): # Está en zona dominada
        return binary_search_x(base, t, args, x, low, mid, depth-1)
    return binary_search_x(base, t, args, x, mid, high, depth-1)

def binary_search_y(base: Cost, t, args: list, y: float, low: float, high: float, depth: int):
    mid = (low + high)/2
    if depth == 0:
        return mid
    
    d1, d2 = transform(t, args, mid, y)
    point = Cost(d1, d2)
    if base.weakly_dominates(point): # Está en zona dominada
        return binary_search_x(base, t, args, y, low, mid, depth-1)
    return binary_search_x(base, t, args, y, mid, high, depth-1)

c1, c2 = transform(t, args, X, Y)
base = Cost(c1, c2)

if len(sys.argv) <= 1 or sys.argv[1] == "full":
    dom_x = []
    dom_y = []
    low_x = []
    low_y = []

    for i in range(RANGE_X*PRECISION):
        for j in range(RANGE_Y*PRECISION):
            d1, d2 = transform(t, args, i/PRECISION, j/PRECISION)
            point = Cost(d1, d2)
            if base.weakly_dominates(point):
                dom_x.append(i/PRECISION)
                dom_y.append(j/PRECISION)
            else:
                low_x.append(i/PRECISION)
                low_y.append(j/PRECISION)

    plt.scatter(dom_x, dom_y, c="blue", s=0.1)
    plt.scatter(low_x, low_y, color="yellow", s=0.1)

    plt.show()

elif sys.argv[1] == "border":
    border_x = []
    border_y = []

    for i in range(RANGE_X*PRECISION):
        x = i/PRECISION
        low_x, low_y = transform(t, args, x, 0)
        low = Cost(low_x, low_y)
        high_x, high_y = transform(t, args, x, RANGE_Y)
        high = Cost(high_x, high_y)
        
        if base.dominates(low) == base.dominates(high):
            continue

        y = binary_search_x(base, t, args, x, 0, RANGE_Y, DEPTH)
        border_x.append(x)
        border_y.append(y)
    
    for i in range(RANGE_Y*PRECISION):
        y = i/PRECISION
        low_x, low_y = transform(t, args, 0, y)
        low = Cost(low_x, low_y)
        high_x, high_y = transform(t, args, RANGE_X, y)
        high = Cost(high_x, high_y)
        
        if base.dominates(low) == base.dominates(high):
            continue

        x = binary_search_y(base, t, args, y, 0, RANGE_X, DEPTH)
        border_x.append(x)
        border_y.append(y)
    
    plt.scatter(border_x, border_y, s=0.1)
    plt.show()
else:
    dom_x = []
    dom_y = []
    dl_x = []
    dl_y = []
    ld_x = []
    ld_y = []
    low_x = []
    low_y = []

    ca1, ca2 = transform(t2, args2, X, Y)
    basea = Cost(ca1, ca2)

    for i in range(RANGE_X*PRECISION):
        for j in range(RANGE_Y*PRECISION):
            d1, d2 = transform(t, args, i/PRECISION, j/PRECISION)
            da1, da2 = transform(t2, args2, i/PRECISION, j/PRECISION)
            point = Cost(d1, d2)
            pointa = Cost(da1, da2)
            if base.weakly_dominates(point):
                if basea.weakly_dominates(pointa):
                    dom_x.append(i/PRECISION)
                    dom_y.append(j/PRECISION)
                else:
                    dl_x.append(i/PRECISION)
                    dl_y.append(j/PRECISION)
            else:
                if basea.weakly_dominates(pointa):
                    ld_x.append(i/PRECISION)
                    ld_y.append(j/PRECISION)
                else:
                    low_x.append(i/PRECISION)
                    low_y.append(j/PRECISION)

    plt.scatter(dom_x, dom_y, c="blue", s=0.1)
    plt.scatter(dl_x, dl_y, c="purple", s=0.1)
    plt.scatter(ld_x, ld_y, c="green", s=0.1)
    plt.scatter(low_x, low_y, color="yellow", s=0.1)

    plt.show()