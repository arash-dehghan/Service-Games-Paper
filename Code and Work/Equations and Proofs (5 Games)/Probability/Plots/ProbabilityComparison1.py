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

PrSR = p*(p**2 + 3*p*q*(p - 1)*(q - 1) + 3*p*(p - 1)*(q - 1) + 3*(p - 1)**2*(q - 1)**2)
PrCR = p*(6*p**2*q**2 - 6*p**2*q + p**2 - 9*p*q**2 + 12*p*q - 3*p + 3*q**2 - 6*q + 3)
PrSRCWMT = p*(-p**3*q + 4*p**2*q**2 - 3*p**2*q + p**2 - p*q**3 - 5*p*q**2 + 9*p*q - 3*p + q**3 + q**2 - 5*q + 3)
PrTR = p*(-p**3*q + p**3 + 4*p**2*q**2 - p**2*q - 2*p**2 - p*q**3 - 4*p*q**2 + 5*p*q + q**3 - 3*q + 2)

SR = PrSR.subs([(p,myval)])
CR = PrCR.subs([(p,myval)])
SRCWMT = PrSRCWMT.subs([(p,myval)])
TR = PrTR.subs([(p,myval)])

print(SR.subs([(q,1/2)]))
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

plt.plot(mylist, SRlist, label='PrSR=PrCR', c = 'red', linestyle = '--')
plt.plot(mylist, SRCWMTlist, label='PrM2', c = 'royalblue')
plt.plot(mylist, TRlist, label='PrTR', c = 'green', linestyle = ':')
plt.plot([0.5],[0.5], 'ro', c ='black', label = 'p+q=1')

plt.xlabel('q')
plt.ylabel('Probability of A Winning')
plt.title('Probability\np={}'.format(str(myval)))
plt.legend()
plt.show()
