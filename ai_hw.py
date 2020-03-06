from time import sleep as sleep
minint = -500000
maxint = 500000

# script to check for a homework for CS 4700: Introduction to AI
# implements minimax with Alpha-Beta pruning

LtoR = 0

# represent tree in a heap manner
f = [0]*15
f.extend([9,3,1,7,3,7,1,5,4,9,3,2,6,4,3,8])  # evaluation scores of the outcome states
# direction of tree expansion
if LtoR:
    expand = lambda x: [x*2+1,x*2+2]
else:
    expand = lambda x: [x*2+2,x*2+1]
assert(len(f)==31)
visited = [0]*31 # boolean array of traversal

# Pretty printing for the tree
# the first tree is the optimal outcome for each player
# the second tree is the record of traversal
def print_tree():
    # first tree
    trees = [f,visited]
    for tree in trees:
        for i in range(31):
            if i in [0,1,3,7,15]:
                out = ""
                if i==0: b,sp = 25,0
                if i==1: b,sp = 14,23
                if i==3: b,sp = 8,11
                if i==7: b,sp = 5,5
                if i==15: b,sp = 3,2
                out = " "*b + str(tree[i])
            else:
                out += " "*sp + str(tree[i])
            if i in [0,2,6,14,30]:
                print(out)
        print("")
    print("\n--------------------------------------------------")

# minimax: my turn
def minimaxAB(s,depth,a,b):
    visited[s] = 1
    if depth==0:
        return f[s]
    else:
        val = minint
        for ch in expand(s):
            valP = maximinAB(ch,depth-1,max(a,val),b)
            if valP >= b:
                f[s] = valP
                print("me")
                print_tree()
                sleep(0.8)
                return valP
            if valP > val:
                val = valP
        f[s] = val
        print("me")
        print_tree()
        sleep(0.8)
        return val

# maximin: opponent's turn
def maximinAB(s,depth,a,b):
    visited[s] = 1
    if depth==0:
        return f[s]
    else:
        val = maxint
        for ch in expand(s):
            valP = minimaxAB(ch,depth-1,a,min(b,val))
            if valP <= a:
                f[s] = valP
                print("enemy")
                print_tree()
                sleep(0.8)
                return valP
            if valP < val:
                val = valP
        f[s] = val
        print("enemy")
        print_tree()
        sleep(0.8)
        return val

# print my best possible outcome as a score
print(minimaxAB(0,4,minint,maxint))
