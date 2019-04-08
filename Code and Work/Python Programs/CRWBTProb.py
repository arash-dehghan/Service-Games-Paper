from __future__ import division
from sympy import *
import math
import xlwings as xw

var('p q A B')

Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
Aserving = ['p','(1-p)']
Bserving = ['q', '(1-q)']
extraAserving = ['A','(1-A)']
extraBserving = ['B','(1-B)']

myAlist = [['p',1,0,1],['(1-p)',0,1,0]]
myBlist = [['q',1,0,1],['(1-q)',0,1,0]]

templist = []
AWinProb = []
BWinProb = []
keeprunning = True
Aequation = ''
Bequation = ''

def CRWBTProbsList(mylist,AorB):
    global templist,Aserving,Bserving, keeprunning, AWinProb, BWinProb, enoughtowin
    while keeprunning == True:
        for x in mylist:
            if x[1]==(enoughtowin-1) and x[2]==(enoughtowin-1):
                if AorB == 1:
                    if x[3]==0:
                        for i in extraAserving:
                            if i=='A':
                                probvalue=str(x[0])+"*"+str(i)
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                                AWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                    elif x[3]==1:
                        for i in extraBserving:
                            if i=='(1-B)':
                                probvalue=str(x[0])+"*"+str(i)
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                                AWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                elif AorB == 0:
                    if x[3]==0:
                        for i in extraBserving:
                            if i=='B':
                                probvalue=str(x[0])+"*"+str(i)
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                                BWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                    elif x[3]==1:
                        for i in extraAserving:
                            if i=='(1-A)':
                                probvalue=str(x[0])+"*"+str(i)
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                                BWinProb.append([probvalue,newAwins,newBwins,lastwinner])
            else:
                if AorB == 1:
                    if x[3]==0:
                        for i in Aserving:
                            if i=='p':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                            if i=='(1-p)':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner=0
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner])
                    elif x[3]==1:
                        for i in Bserving:
                            if i=='q':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner=0
                            if i=='(1-q)':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner])
                elif AorB == 0:
                    if x[3]==0:
                        for i in Bserving:
                            if i=='q':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                            if i=='(1-q)':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner=0
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner])
                    elif x[3]==1:
                        for i in Aserving:
                            if i=='p':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner=0
                            if i=='(1-p)':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner=1
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner])
        if AorB == 1:
            for i in templist:
                if i[1]==enoughtowin:
                    AWinProb.append(i)
                    templist.remove(i)
            for i in templist:
                if i[2]==enoughtowin:
                    templist.remove(i)
        elif AorB == 0:
            for i in templist:
                if i[1]==enoughtowin:
                    BWinProb.append(i)
                    templist.remove(i)
            for i in templist:
                if i[2]==enoughtowin:
                    templist.remove(i)
        mylist = templist
        templist = []

        if len(mylist)==0:
            keeprunning = False
        else:
            CRWBTProbsList(mylist,AorB)

def CRWBTProbsEquation():
    global AWinProb,BWinProb,Aequation, Bequation, enoughtowin
    for i in AWinProb:
        Aequation += i[0]+"+"
    for i in BWinProb:
        Bequation += i[0]+"+"
    Aequation = expand(Aequation[0:len(Aequation)-1])
    Bequation = expand(Bequation[0:len(Bequation)-1])
    CRWBTFinalEquation()

def CRWBTFinalEquation():
    global Aequation, Bequation
    A = Symbol('A')
    B = Symbol('B')
    p = Symbol('p')
    q = Symbol('q')

    APr = Aequation
    Aanswer = Eq(APr,A)
    Aanswer = solve(Aanswer,B)
    Aanswer = Aanswer[0]

    BPr = Bequation
    Banswer = Eq(BPr,B)
    Banswer = solve(Banswer,B)
    Banswer = Banswer[0]

    final = Eq(Banswer,Aanswer)
    final = solve(final,A)
    final = final[0]
    CRWBTMakeValues(final,enoughtowin)

def CRWBTMakeValues(equation,enoughtowin):
    global Values
    valueslist=[]
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every probability value we get to two decimal points
            value = round(equation.subs([(p,Values[x]),(q,Values[y])]),2)
            valueslist.append(value)
    CRWBTMakeExcel(valueslist,enoughtowin)

def CRWBTMakeExcel(valueslist,enoughtowin):
    global Values
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    #Here we are filling our table with the data we recieve from our valueslist function. Using a double for loop to
    #loop through each combination of p and q value and assign the corresponding probabilities to it in the table
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
    sht.cells(12,12).value = "DNE"
    #Finally, we just want to add in a cell the 2k+1 series game for which we are calculating our data
    sht.cells(1,15).value = ("{}-game CR WBT series").format((2*enoughtowin)-1)

enoughtowin = 5

CRWBTProbsList(myAlist,1)
keeprunning = True
CRWBTProbsList(myBlist,0)
CRWBTProbsEquation()
