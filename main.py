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
#args = {"type": "func"}

t = "ab" # Transformación alfa-beta
args = {"type": "func", "a": 0.8, "b": 0.8}

#t = "ar" # Transformación alfa-r
#args = {"type": "func", "a": 0.8, "r": 0.5}

#t = "asin" # Transformación alfa-seno
#args = {"type": "func", "a": 0.8}

#t = "epsilon" # Poda epsilon
#args = {"type": "rel", "e": 0.3}

#t = "epsilon-con" # Poda epsilon-consistente
#args = {"type": "rel", "e": 0.3, "m": 1}

t2 = "normal"
args2 = {"type": "func"}

class Cost:
    def __init__(self, c1, c2):
        self.c1 = c1
        self.c2 = c2

    def dominates(self, other):
        return (self.c1 < other.c1 or self.c2 < other.c2) and self.weakly_dominates(other)
    
    def weakly_dominates(self, other):
        return self.c1 <= other.c1 and self.c2 <= other.c2
    
    def epsilon_dominates(self, other, epsilon: float):
        return (self.c1 <= other.c1*(1 + epsilon) and self.c2 < other.c2*(1 + epsilon)) or (
            self.c1 < other.c1*(1 + epsilon) and self.c2 <= other.c2*(1 + epsilon)
        )
    
    def epsilon_con_dominates(self, other, epsilon: float, m: float):
        if other.c1 < self.c1 - self.c2*epsilon/m:
            return False
        if other.c1 <= self.c1:
            return other.c2 > self.c2 + (self.c1-other.c1)*m
        if other.c1 < self.c1 + self.c2*epsilon/m:
            return other.c2 > self.c2 - (other.c1-self.c1)*m
        return other.c2 > self.c2*(1-epsilon)


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
        
def dom_args(u: Cost, v: Cost, t: str, args: list):
    if args["type"] == "func":
        u = Cost(*transform(t, args, u.c1, u.c2))
        v = Cost(*transform(t, args, v.c1, v.c2))
        return u.dominates(v)
    
    match t:
        case "epsilon":
            return u.epsilon_dominates(v, args["e"])
        case "epsilon-con":
            return u.epsilon_con_dominates(v, args["e"], args["m"])
    

def binary_search_x(base: Cost, t, args: list, x: float, low: float, high: float, depth: int):
    mid = (low + high)/2
    if depth == 0:
        return mid
    
    point = Cost(x, mid)
    if dom_args(base, point, t, args): # Está en zona dominada
        return binary_search_x(base, t, args, x, low, mid, depth-1)
    return binary_search_x(base, t, args, x, mid, high, depth-1)

def binary_search_y(base: Cost, t, args: list, y: float, low: float, high: float, depth: int):
    mid = (low + high)/2
    if depth == 0:
        return mid
    
    point = Cost(mid, y)
    if dom_args(base, point, t, args): # Está en zona dominada
        return binary_search_x(base, t, args, y, low, mid, depth-1)
    return binary_search_x(base, t, args, y, mid, high, depth-1)

base = Cost(X, Y)

if len(sys.argv) <= 1 or sys.argv[1] == "full":
    dom_x = []
    dom_y = []
    low_x = []
    low_y = []

    for i in range(RANGE_X*PRECISION):
        for j in range(RANGE_Y*PRECISION):
            point = Cost(i/PRECISION, j/PRECISION)
            if dom_args(base, point, t, args):
                dom_x.append(i/PRECISION)
                dom_y.append(j/PRECISION)
            else:
                low_x.append(i/PRECISION)
                low_y.append(j/PRECISION)

    plt.scatter(dom_x, dom_y, c="blue", s=0.1)
    plt.scatter(low_x, low_y, c="yellow", s=0.1)

elif sys.argv[1] == "border":
    border_x = []
    border_y = []

    for i in range(RANGE_X*PRECISION):
        x = i/PRECISION
        low = Cost(x, 0)
        high = Cost(x, RANGE_Y)
        
        if dom_args(base, low, t, args) == dom_args(base, high, t, args):
            continue

        y = binary_search_x(base, t, args, x, 0, RANGE_Y, DEPTH)
        border_x.append(x)
        border_y.append(y)
    
    for i in range(RANGE_Y*PRECISION):
        y = i/PRECISION
        low = Cost(0, y)
        high = Cost(RANGE_X, y)
        
        if dom_args(base, low, t, args) == dom_args(base, high, t, args):
            continue

        x = binary_search_y(base, t, args, y, 0, RANGE_X, DEPTH)
        border_x.append(x)
        border_y.append(y)
    
    plt.scatter(border_x, border_y, s=0.1)

else:
    dom_x = []
    dom_y = []
    dl_x = []
    dl_y = []
    ld_x = []
    ld_y = []
    low_x = []
    low_y = []

    for i in range(RANGE_X*PRECISION):
        for j in range(RANGE_Y*PRECISION):
            point = Cost(i/PRECISION, j/PRECISION)
            if dom_args(base, point, t, args):
                if dom_args(base, point, t2, args2):
                    dom_x.append(i/PRECISION)
                    dom_y.append(j/PRECISION)
                else:
                    dl_x.append(i/PRECISION)
                    dl_y.append(j/PRECISION)
            else:
                if dom_args(base, point, t2, args2):
                    ld_x.append(i/PRECISION)
                    ld_y.append(j/PRECISION)
                else:
                    low_x.append(i/PRECISION)
                    low_y.append(j/PRECISION)

    plt.scatter(dom_x, dom_y, c="blue", s=0.1)
    plt.scatter(dl_x, dl_y, c="purple", s=0.1)
    plt.scatter(ld_x, ld_y, c="green", s=0.1)
    plt.scatter(low_x, low_y, color="yellow", s=0.1)

plt.scatter(X, Y, c="red")

if len(sys.argv) >= 3:
    plt.savefig(sys.argv[2]) 
else:
    plt.show()