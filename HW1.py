import math

##homework 1

#number 1
#make fib

def fib1(n):
    if n < 2:
        return n
    return fib1(n-2) + fib1(n-1)



##problem 2

def sum1(n):
    if n == 0:
        return(total)
    else:
        total = 0
        while(n>0):
            total += n
            n = n-1
        print(total)

##problem 3

def transpose(matrix):
    n = 0
    List1 = []
    while n < (len(matrix[0])):
        List2 = []
        for sets in matrix:
            List2.append(sets[n])
        List1.append(List2)
        n+=1
    return List1



            


##4

def euclidean(p1,p2):
    Sum = 0
    n=0
    while n < (len(p1)):
        for sets in (p1,p2):
            number = (p2[n]-p1[n])**(2)
            Sum += number
        n += 1
    return (math.sqrt(Sum/2))



##5

##make tree
##get the node data/value
 ##take each node to iterate
##add the sum

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    

##6

    def compose(f, g):
        return lambda x: f(g(x))


def add1(x):
    return x + 1
def square(x):
    return x * 10
    


   
    
    
    
    
    
    

