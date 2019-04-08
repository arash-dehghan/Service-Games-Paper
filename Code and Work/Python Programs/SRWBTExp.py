from __future__ import division
from sympy import *
import math
import xlwings as xw

var('p q A B')
ELSR = Symbol('ELSR')

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
equation = ''

def SRWBTExpList(mylist):
        global templist,Aserving,Bserving, keeprunning, AWinProb, BWinProb, enoughtowin
        while keeprunning == True:
                for x in mylist:
                        if x[1]==(enoughtowin-1) and x[2]==(enoughtowin-1):
                                if x[3]==1:
                                        for i in extraAserving:
                                                if i=='A':
                                                        #probvalue=str(x[0])+"*"+str(i)
                                                        probvalue=str(x[0])
                                                        newAwins=x[1]
                                                        newBwins=x[2]
                                                        lastwinner=x[3]
                                                        AWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                                                #if i=='(1-A)':
                                                #    probvalue=str(x[0])+"*"+str(i)
                                                #    newAwins=x[1]
                                                #    newBwins=x[2]+1
                                                #    lastwinner=0
                                                #    AWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                                elif x[3]==0:
                                        for i in extraBserving:
                                                #if i=='B':
                                                #    probvalue=str(x[0])+"*"+str(i)
                                                #    newAwins=x[1]
                                                #    newBwins=x[2]+1
                                                #    lastwinner=0
                                                #    AWinProb.append([probvalue,newAwins,newBwins,lastwinner])
                                                if i=='(1-B)':
                                                        #probvalue=str(x[0])+"*"+str(i)
                                                        probvalue=str(x[0])
                                                        newAwins=x[1]
                                                        newBwins=x[2]
                                                        lastwinner=x[3]
                                                        AWinProb.append([probvalue,newAwins,newBwins,lastwinner])

                        else:
                                if x[3]==1:
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
                                elif x[3]==0:
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

                for i in templist:
                        if i[1]==enoughtowin:
                                AWinProb.append(i)
                                templist.remove(i)
                for i in templist:
                        if i[2]==enoughtowin:
                                AWinProb.append(i)
                                templist.remove(i)

                mylist = templist
                templist = []

                if len(mylist)==0:
                        keeprunning = False
                        SRWBTExpEquation()
                else:
                        SRWBTExpList(mylist)

def SRWBTExpEquation():
        global AWinProb, enoughtowin, equation
        print(AWinProb)
        for i in AWinProb:
                numberofgames = i[1]+i[2]
                if i[1]==enoughtowin-1 and i[2]==enoughtowin-1:
                    equation += "("+str(2 + ELSR)+")"+"*("+i[0]+")+"
                else:
                    equation += str(numberofgames)+"*("+i[0]+")+"

        equation = equation[0:len(equation)-1]
        print(equation)
        #equation = expand(equation)
        #equation = Eq(equation,ELSR)
        #equation = solve(equation, ELSR)[0]
        #solution = equation.subs([(p,0.75),(q,0.75)])
        #print(solution)
        #SRWBTExpResults()

#def SRWBTExpResults():
#    global equation
#    equation = Eq(equation, ELSR)
#    equation = solve(equation)
#    print(equation)

enoughtowin = 3
SRWBTExpList(myAlist)
#print(AWinProb)
