from sympy import *
import math
import xlwings as xw

var('p q')

totaloptions = ['p','1-p','q','1-q']
Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
Aserving = ['p','(1-p)']
Bserving = ['q', '(1-q)']

#Wins = [Probability thus far, A's current scores, B's current score, A's score prior to this, B's score prior to this]
mylist = [['p',1,0,0,0],['(1-p)',0,1,0,0]]
templist = []
bwinslist = []
keeprunning = True

def TRaProbsList(enoughtowin):
    global templist,mylist,Aserving,Bserving, keeprunning, bwinslist
    while keeprunning == True:
        for x in mylist:
            if x[1]==enoughtowin or x[2]==enoughtowin:
                templist.append(x)
            else:
                if x[1]>x[2]:
                    prevAwins=x[1]
                    prevBwins=x[2]
                    for i in Bserving:
                        if i=='q':
                            newAwins=x[1]
                            newBwins=x[2]+1
                        if i=='(1-q)':
                            newAwins=x[1]+1
                            newBwins=x[2]
                        probvalue=str(x[0])+"*"+str(i)
                        templist.append([probvalue,newAwins,newBwins,prevAwins,prevBwins])
                elif x[1]<x[2]:
                    prevAwins=x[1]
                    prevBwins=x[2]
                    for i in Aserving:
                        if i=='p':
                            newAwins=x[1]+1
                            newBwins=x[2]
                        if i=='(1-p)':
                            newAwins=x[1]
                            newBwins=x[2]+1
                        probvalue=str(x[0])+"*"+str(i)
                        templist.append([probvalue,newAwins,newBwins,prevAwins,prevBwins])
                elif x[1]==x[2]:
                    if x[3]>x[4]:
                        prevAwins=x[1]
                        prevBwins=x[2]
                        for i in Aserving:
                            if i=='p':
                                newAwins=x[1]+1
                                newBwins=x[2]
                            if i=='(1-p)':
                                newAwins=x[1]
                                newBwins=x[2]+1
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,prevAwins,prevBwins])
                    elif x[3]<x[4]:
                        prevAwins=x[1]
                        prevBwins=x[2]
                        for i in Bserving:
                            if i=='q':
                                newAwins=x[1]
                                newBwins=x[2]+1
                            if i=='(1-q)':
                                newAwins=x[1]+1
                                newBwins=x[2]
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,prevAwins,prevBwins])

        for i in templist:
            if i[2]==enoughtowin:
                templist.remove(i)
                bwinslist.append(i)
        mylist = templist
        templist = []

        total = 0
        for i in mylist:
            total += abs(i[1]-enoughtowin)
        for i in bwinslist:
            total += abs(i[2]-enoughtowin)
        if total == 0:
            keeprunning = False
            TRaProbsEquation(enoughtowin)
        else:
            TRaProbsList(enoughtowin)

def TRaProbsEquation(enoughtowin):
    global mylist
    print(mylist)
    equation = ''
    for i in mylist:
        equation += i[0]+"+"
    print(equation)
    equation = simplify(equation[0:len(equation)-1])
    print(equation)
    #print("Here is the simplified equation for calculating the probability of a {}-Game set under TRa Rules:".format(2*enoughtowin-1))
    #print(equation)
    #TRaMakeValues(equation,enoughtowin)

def TRaMakeValues(equation,enoughtowin):
    global Values
    valueslist=[]
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every probability value we get to two decimal points
            value = round(equation.subs([(p,Values[x]),(q,Values[y])]),2)
            valueslist.append(value)
    TRaMakeExcel(valueslist,enoughtowin)
def TRaMakeExcel(valueslist,enoughtowin):
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
    #Finally, we just want to add in a cell the 2k+1 series game for which we are calculating our data
    sht.cells(1,15).value = ("{}-game TRa series").format((2*enoughtowin)-1)


TRaProbsList(5)
