from bisect import bisect_left

def index(a, x):
    """Locate the leftmost value exactly equal to x"""
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return i
    raise ValueError

#fd = open( "input00.txt" )
#raw_input = fd.readline

#!/bin/python



# code snippet for illustrating input/output

N = int(raw_input())

s = []
x = []

for i in range(0, N):

    tmp = raw_input()
    a, b = [xx for xx in tmp.split(' ')]
    s.append(a)
    x.append(int(b))

sorted_list = []

def add(e):
    if not len(sorted_list):
        sorted_list.append(e)
        return

    i = bisect_left(sorted_list, e)
    sorted_list.insert(i, e)

def remove(e):
    sorted_list.remove(e)

def median():
    l = len(sorted_list)
    if not l:
        raise ValueError

    if l % 2 == 0:
        n = (sorted_list[l / 2] + sorted_list[l / 2 - 1]) / float(2)
    else:
        n = sorted_list[int(l / 2)]

    if n == int(n):
        print str(int(n))
    else:
        print n

for i in range(0, N):
    try:
        if s[i] == 'a' :
            add(x[i])
        else:
            remove(x[i])
        median()
    except ValueError:
        print "Wrong!"