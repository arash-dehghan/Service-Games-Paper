from sympy import *
import math
import xlwings as xw

var('p q')

totaloptions = ['p','1-p','q','1-q']
Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
Aserving = ['p','(1-p)']
Bserving = ['q', '(1-q)']

#Wins = [Probability thus far, A's current scores, B's current score, A's score prior to this, B's score prior to this]
mylist = [['p',1,0,1,1,0],['(1-p)',0,1,0,0,1]]
templist = []
keeprunning = True
bwinslist = []
mytotal = 0

def SRExpList(enoughtowin,cantwinmorethan):
    global templist,mylist,Aserving,Bserving, keeprunning, mytotal, myx
    while keeprunning == True:
        for x in mylist:
            if x[1]==enoughtowin:
                templist.append(x)
            elif x[2]==enoughtowin:
                bwinslist.append(x)
            else:
                mytotal = x[4]+x[5]
                if cantwinmorethan>mytotal:
                    if x[3]==0:
                        for i in Bserving:
                            if i=='q':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner = 0
                                Astreak = 0
                                Bstreak = x[5] + 1
                            if i=='(1-q)':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner = 1
                                Astreak = x[4] + 1
                                Bstreak = 0
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner,Astreak,Bstreak])
                    elif x[3]==1:
                        for i in Aserving:
                            if i=='p':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner = 1
                                Astreak = x[4] + 1
                                Bstreak = 0
                            if i=='(1-p)':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner = 0
                                Astreak = 0
                                Bstreak = x[5] + 1
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner, Astreak, Bstreak])
                if cantwinmorethan<=mytotal:
                    if x[5]>=cantwinmorethan:
                        for i in Aserving:
                            if i=='p':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner = 1
                                Astreak = x[4]+1
                                Bstreak = 0
                            if i=='(1-p)':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner = 0
                                Astreak = 0
                                Bstreak = 1
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner,Astreak,Bstreak])
                    elif x[4]>=cantwinmorethan:
                        for i in Bserving:
                            if i=='q':
                                newAwins=x[1]
                                newBwins=x[2]+1
                                lastwinner = 0
                                Astreak = 0
                                Bstreak = 1
                            if i=='(1-q)':
                                newAwins=x[1]+1
                                newBwins=x[2]
                                lastwinner = 1
                                Astreak = x[4]+1
                                Bstreak = 0
                            probvalue=str(x[0])+"*"+str(i)
                            templist.append([probvalue,newAwins,newBwins,lastwinner, Astreak, Bstreak])
                mytotal=0
        for i in templist:
            if i[2]==enoughtowin:
                bwinslist.append(i)
                templist.remove(i)
        mylist = templist
        templist = []

        total = 0
        for i in mylist:
            total += abs(i[1]-enoughtowin)
        for i in bwinslist:
            total += abs(i[2]-enoughtowin)
        if total == 0:
            keeprunning = False
            for i in bwinslist:
                mylist.append(i)
            print(mylist)
            SRExpEquation(enoughtowin,cantwinmorethan)
        else:
            SRExpList(enoughtowin,cantwinmorethan)

def SRExpEquation(enoughtowin,cantwinmorethan):
    global mylist
    equation = ''
    for i in mylist:
        numberofgames = i[1]+i[2]
        equation += str(numberofgames)+"*("+i[0]+")+"
    print(equation)
    equation = expand(equation[0:len(equation)-1])
    print("Here is the simplified equation for calculating the expected length of a {}-Game set under SR Rules with Can't Win More Than {}:".format(2*enoughtowin-1,cantwinmorethan))
    print(factor(equation))
    #SRMakeValues(equation,enoughtowin,cantwinmorethan)

def SRMakeValues(equation,enoughtowin,cantwinmorethan):
    global Values
    valueslist=[]
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every probability value we get to two decimal points
            value = round(equation.subs([(p,Values[x]),(q,Values[y])]),2)
            valueslist.append(value)
    SRMakeExcel(valueslist,enoughtowin,cantwinmorethan)
def SRMakeExcel(valueslist,enoughtowin,cantwinmorethan):
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
    sht.cells(1,15).value = ("{}-game SR series with Can't Win More Than {} games in a row.").format((2*enoughtowin)-1,cantwinmorethan)


SRExpList(3,3)
