from __future__ import division
from sympy import *
import math
import xlwings as xw
import matplotlib.pyplot as plt
#from sympy import Eq, Symbol, solve

#var('p q r s A B')
A = Symbol('A')
B = Symbol('B')
p = Symbol('p')
q = Symbol('q')
r = Symbol('r')
x = Symbol('x')
ELSR = Symbol('ELSR')

myval = round(1/2,3)
mylist = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
SRlist = []
CRlist = []
SRCWMTlist = []
TRlist = []

ExpSR = -3*p**3*q + p**3 + 3*p**2*q**2 + p**2*q - 3*p**2 - 3*p*q**2 + 4*p*q - 2*q + 5
ExpCR = -3*p**3*q + 2*p**3 + 3*p**2*q**2 + 2*p**2*q - 5*p**2 - 3*p*q**2 + 3*p*q + 3*p + 3
ExpSRCWMT = -3*p**3*q + p**3 + 3*p**2*q**2 + p**2*q - 2*p**2 - 3*p*q**2 + 6*p*q - p + q**2 - 3*q + 5
ExpTR = p**4 - 2*p**3*q - p**3 + 2*p**2*q**2 + p**2*q - 2*p**2 - p*q**3 - p*q**2 + 3*p*q + 2*p + 3

SR = ExpSR.subs([(p,myval)])
CR = ExpCR.subs([(p,myval)])
SRCWMT = ExpSRCWMT.subs([(p,myval)])
TR = ExpTR.subs([(p,myval)])
#print(SR.subs([(q,0.5)]))

for qnum in mylist:
    number = SR.subs([(q,qnum)])
    SRlist.append(round(number,3))

for qnum in mylist:
    number = CR.subs([(q,qnum)])
    CRlist.append(round(number,3))

for qnum in mylist:
    number = SRCWMT.subs([(q,qnum)])
    SRCWMTlist.append(round(number,3))

for qnum in mylist:
    number = TR.subs([(q,qnum)])
    TRlist.append(round(number,3))

plt.plot(mylist, SRlist, label='ELSR', c = 'red', linestyle = '--')
plt.plot(mylist, CRlist, label='ELCR', c = 'purple', linestyle = '-.')
plt.plot(mylist, SRCWMTlist, label='ELM2', c = 'royalblue', )
plt.plot(mylist, TRlist, label='ELTR', c = 'green', linestyle = ':')
plt.plot([0.5],[4.125], 'ro', c ='black', label = 'p+q=1')

plt.xlabel('q')
plt.ylabel('Expected Length of Game')
plt.title('Expected Length\np={}'.format(str(myval)))
plt.legend()
plt.show()
