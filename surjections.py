import numpy as np
import math
from scipy.special import comb

# this script solves the question:
#   How many distinct surjections f:A->B are there if |A|=m > |B|=n?

# take inputs
flag = True
while flag:
	try:
		m = int(input('type an integer m  : \n'))
		n = int(input('type an integer n<m: \n'))
		if m<n:
			(m,n) = (n,m)
			print('you input m<n, so the values were switched')
	except _ as _:
		print('your inputs were not valid, please try again:\n\n')


# use dynamic programming:
# A function from A to B is not a surjection if at least one element of B has no corresponding input in A,
#   or if the function is a surjection from A to B', a strict subset of B.
# Constructing such a function requires selecting B', of which there are |B| choose |B'|,
#   and counting the surjections from A to B'.

# m_surj[i] = "num of surjections from A to B, where |A|=m and |B|=i".
m_surj = [0,1]
for i in range(2,n+1):
	# sum the number of non-surjections.
	non_surj = sum([comb(i,k,exact = True)*m_surj[k] for k in range(1,i)])
	# subtract this number from the total number of functions, which is i^m.
	m_surj.append(i**m - non_surj)
del(m_surj[0])

# The result!
print(m_surj)