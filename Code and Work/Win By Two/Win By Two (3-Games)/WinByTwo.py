from __future__ import division
import numpy as np
from sympy import *
import math
import xlwings as xw
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style

var('p q X Y')
Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
pvalues = []
qvalues = []
valueslist = []

######################################################################################################################

#Recall the follow:
#PrSR(A) - > Probability that A wins when A serves first
#PrSR(B) - > Probability that B wins when B serves first
#1 - PrSR(A) - > Probability that B wins when A serves first
#1 - PrSR(B) - > Probability that A wins when B serves first
#When we try to solve for PrSR(A) and PrSR(B) in a 3-game series (k=1) we arrive at the following two recursive formulas
PrSR(A) = (p**2)+(p)(1-p)(1-PrSR(B))+(1-p)(1-q)(PrSR(A))
PrSR(B) = (q**2)+(q)(1-q)(1-PrSR(A))+(1-q)(1-p)(PrSR(B))
#Next we try to solve these two equations for PrSR(A) and PrSR(B), where we end up getting the following:
#PrSR(A) = -(p**2)/((p**2)*(q)-(p**2)+(p)*(q**2)-(p)*(q)-(q**2))
#PrSR(B) = -(q**2)/((p**2)*(q)-(p**2)+(p)*(q**2)-(p)*(q)-(q**2))
#We can see that these are the correct equations by plugging in p=q and solving, for example, PrSR(A) at p=1/3 and q=1/3 equals the same as the equation we're given in the paper
def PrSrA(p,q):
    value = round(-(p**2)/((p**2)*(q)-(p**2)+(p)*(q**2)-(p)*(q)-(q**2)),2)
    if value == -0.0:
        return 0.0
    else:
        return value

def PrSrB(p,q):
    value = round(-(q**2)/((p**2)*(q)-(p**2)+(p)*(q**2)-(p)*(q)-(q**2)),2)
    if value == -0.0:
        return 0.0
    else:
        return value

#Now we do the same thing for PrCrA and PrCrB, where originally we have:
PrCR(A) = (p)(1-q)+(p)(q)(PrCR(A))+(1-p)(p)(1-PrCR(B))
PrCR(B) = (q)(1-p)+(q)(p)(PrCR(B))+(1-q)(q)(1-PrSR(A))
#Now we solve these equations for PrCR(A) and PrCR(B) to arrive at:
#PrCR(A) = ((p)*(q-1)*(p+q-2))/((p**2)*(q)+(p)*(q-3)*(q)+1)
#PrCR(B) = ((q)*(p-1)*(p+q-2))/((p**2)*(q)+(p)*(q-3)*(q)+1)

def PrCrA(p,q):
    value = round(((p)*(q-1)*(p+q-2))/((p**2)*(q)+(p)*(q-3)*(q)+1),2)
    if value == -0.0:
        return 0.0
    else:
        return value

def PrCrB(p,q):
    value = round(((q)*(p-1)*(p+q-2))/((p**2)*(q)+(p)*(q-3)*(q)+1),2)
    if value == -0.0:
        return 0.0
    else:
        return value

#Now lets try this for the expected length of games, under SR and CR. We originally have the equation:
ELSR = ((p**2)+(1-p)(q))(2)+((p)(1-p)+(1-p)(1-q))(ELSR + 2)
ELCR = ((p)(1-q)+((1-p)^2))(2)+((p)(q)+(1-p)(p))(ELCR + 2)
#Now we solve the equations for ELSR and ELCR
#ELSR = 2 / (p**2 - p * q + q)
#ELCR = 2 / (p**2 - p * (q+1) + 1)

def ELSR(p,q):
    value = round((2 / (p**2 - p * q + q)),2)
    if value == -0.0:
        return 0.0
    else:
        return value

def ELCR(p,q):
    value = round((2 / (p**2 - p * (q+1) + 1)),2)
    if value == -0.0:
        return 0.0
    else:
        return value

######################################################################################################################

def SrAValues():
    valueslist = []
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            try:
                valueslist.append(PrSrA(Values[x],Values[y]))
            except ZeroDivisionError:
                valueslist.append("DNE")
            pvalues.append(Values[x])
            qvalues.append(Values[y])
    return valueslist,pvalues,qvalues

def CrAValues():
    valueslist = []
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            try:
                valueslist.append(PrCrA(Values[x],Values[y]))
            except ZeroDivisionError:
                valueslist.append("DNE")
            pvalues.append(Values[x])
            qvalues.append(Values[y])
    return valueslist,pvalues,qvalues

def SRELValues():
    valueslist = []
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            try:
                valueslist.append(ELSR(Values[x],Values[y]))
            except ZeroDivisionError:
                valueslist.append("Infinity")
            pvalues.append(Values[x])
            qvalues.append(Values[y])
    return valueslist,pvalues,qvalues

def CRELValues():
    valueslist = []
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            try:
                valueslist.append(ELCR(Values[x],Values[y]))
            except ZeroDivisionError:
                valueslist.append("Infinity")
            pvalues.append(Values[x])
            qvalues.append(Values[y])
    return valueslist,pvalues,qvalues
######################################################################################################################

def SrAMakeExcel():
    val,pee,que = SrAValues()
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = val[count]
            count = count+1
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    sht.cells(1,15).value = ("3-Game SR Win-By-Two Game")


def CrAMakeExcel():
    val,pee,que = CrAValues()
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = val[count]
            count = count+1
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    sht.cells(1,15).value = ("3-Game CR Win-By-Two Game")

def SRELMakeExcel():
    val,pee,que = SRELValues()
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = val[count]
            count = count+1
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    sht.cells(1,15).value = ("3-Game SR Win-By-Two Game Expected Length")

def CRELMakeExcel():
    val,pee,que = CRELValues()
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = val[count]
            count = count+1
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    sht.cells(1,15).value = ("3-Game CR Win-By-Two Game Expected Length")

######################################################################################################################

def SrAMakePlots():
    zee,ex,why= SrAValues()
    style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    del ex[0]
    del why[0]
    del zee[0]
    x = ex
    y = why
    z = zee
    ax1.scatter(x, y, z, c='g', marker='o')
    ax1.set_xlabel('p-values')
    ax1.set_ylabel('q-values')
    ax1.set_zlabel('SR Probability')
    ax1.set_title("Standard Rule Win-By-Two Probability Scatter Plot")
    plt.show()

def CrAMakePlots():
    zee,ex,why= CrAValues()
    style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    del ex[-1]
    del why[-1]
    del zee[-1]
    x = ex
    y = why
    z = zee
    ax1.scatter(x, y, z, c='g', marker='o')
    ax1.set_xlabel('p-values')
    ax1.set_ylabel('q-values')
    ax1.set_zlabel('CR Probability')
    ax1.set_title("Catch-Up Rule Win-By-Two Probability Scatter Plot")
    plt.show()

def SRELMakePlots():
    zee,ex,why= SRELValues()
    style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    del ex[0]
    del why[0]
    del zee[0]
    x = ex
    y = why
    z = zee
    ax1.scatter(x, y, z, c='g', marker='o')
    ax1.set_xlabel('p-values')
    ax1.set_ylabel('q-values')
    ax1.set_zlabel('SR Expected Length')
    ax1.set_title("Standard Rule Win-By-Two Expected Length Scatter Plot")
    plt.show()

def CRELMakePlots():
    zee,ex,why= CRELValues()
    style.use('ggplot')
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    del ex[-1]
    del why[-1]
    del zee[-1]
    x = ex
    y = why
    z = zee
    ax1.scatter(x, y, z, c='g', marker='o')
    ax1.set_xlabel('p-values')
    ax1.set_ylabel('q-values')
    ax1.set_zlabel('CR Expected Length')
    ax1.set_title("Catch-Up Rule Win-By-Two Expected Length Scatter Plot")
    plt.show()

######################################################################################################################

CRELMakePlots()
