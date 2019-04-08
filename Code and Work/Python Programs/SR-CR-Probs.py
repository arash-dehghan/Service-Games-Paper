from __future__ import division
from sympy import *
import math
import xlwings as xw

var('p q')
Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

def Combos(n,r):
    return math.factorial(n)/((math.factorial(r))*math.factorial(n-r))

def ProbsFront(aservewins, bservewins, k):
    #Here, if our 'if' statement is true, we return the value zero. This is relevant when performing our combinations
    #For example, if either of these statements are true, we will not be able to take the combinations of the values (will return an error for 2C3 for example)
    #So instead, we return zero, this becomes relavent when we begin multiplying this ProbsFront value, since we want to exlude
    #and instance of these aservewins and bservewins combinations, multiplying by zero will do this for us
    if aservewins > (k+1) or bservewins > k:
        return 0
    else:
        return int(Combos(k+1,aservewins)*Combos(k,bservewins))

def ProbsEnd(aservewins, bservewins, k):
    equation = (p**aservewins)*((1-p)**(k + 1 - aservewins))*(q**bservewins)*((1-q)**(k - bservewins))
    return equation

#Finally, we can use the Probabilities function to calculate the probability of any particular situation taking place
#For examples, the probability of A winning 2 serves while B wins 0 serves in a best of 3 series
#This will return to us an equation for calucating this probability for any values of p and q
def Probabilities(aservewins, bservewins, k):
    #This is where our returning of zero for ProbsFront becomes relavent, as we are multiplying by zero and essentially getting rid of this combination
    return ProbsFront(aservewins, bservewins, k) * ProbsEnd(aservewins, bservewins, k)

def SRCRMakeValues(equation,enoughtowin):
    global Values
    valueslist=[]
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every expected length value we get to two decimal points
            value = round(equation.subs([(p,Values[x]),(q,Values[y])]),10)
            valueslist.append(value)
    SRCRMakeExcel(valueslist,enoughtowin)

def SRCRMakeExcel(valueslist,enoughtowin):
    global Values
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    #Here we are filling our table with the data we recieve from our CRReturningValues function. Using a double for loop to
    #loop through each combination of p and q value and assign the corresponding expected length to it in the table
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = valueslist[count]
            count = count+1
    #We are doing a for loop now to fill the labels/brackets of our table (placing the p and q values)
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    #Finally, we just want to add in a cell the 2k+1 series game for which we are calculating our data
    sht.cells(1,15).value = ("{}-game SR/CR series").format((2*enoughtowin)-1)

def SRCRGetEquation(k):
    probeq=0
    for x in range(0,k+2):
        for y in range(0,k+2):
            if y<x:
                probeq += Probabilities(x,y,k)
    print(probeq)
    equation = simplify(probeq)
    print("Here is the simplified equation for calculating the probability of a {}-Game set under SR/CR Rules:".format(2*k+1))
    print(equation)
    SRCRMakeValues(equation,k+1)

SRCRGetEquation(2)
