#To run this program you may need to pip install sympy and xlwings
#Its important to note that NumPy arrays could have also been used, but were not.
from __future__ import division
from sympy import *
import math
import xlwings as xw

#######################################################################################################
#The variables, p and q, which we will be using in our expected length equations. p represents player A's probability of winning their serve.
#q represents player B's probability of winning their serve (Important to note that q does not equal 1-p)
var('p q')
#Initializing our list of p and q values we want data for
Values = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
#Initializing the empty lists which we will be using in our functions
SRNewList = []
SREvalues = []
CRNewList = []
CREvalues = []
pvalues = []
qvalues = []

#######################################################################################################

#In this section I am just setting up some of the basic tools we will need for calculating the expected length of any 2k+1 game

#Combos just calculates combinations, when given an n and r value as input, later we will be using these n and r values as
#serves that player A or B wins
def Combos(n,r):
    return math.factorial(n)/((math.factorial(r))*math.factorial(n-r))

#The rest of these are just calculating different parts of our final formula which we will need, all of these formulas can be found
#around pages 18 and 19 in the paper

def SRExpectedDigit(aservewins, bservewins, k):
    if aservewins>bservewins:
        return (2*(k+1))-(aservewins - bservewins)*( ((bservewins) / (k+1-bservewins))+1 )
    else:
        return (2*(k+1))-(bservewins - aservewins + 1)*( ((aservewins) / (k+1-aservewins+1))+1 )

def CRExpectedDigit(aservewins, bservewins, k):
    if aservewins>bservewins:
        return (2*(k+1))-(aservewins - bservewins)*( ((k+1-aservewins) / (aservewins+1))+1 )
    else:
        return (2*(k+1))-(bservewins - aservewins + 1)*( ((k-bservewins) / (bservewins+1))+1 )


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

#######################################################################################################

#This next portion is used to derive and output the equations/formulas for the expected length of a 2k+1 series
#Similar to the probabilities function, the functions below return an equation

#This is the function which will return to you the equation of the expected length of a 2k+1 length game with Standard Rules
#You enter in your k-value, for example k=1 for a 3-game series, and it will return to you the equation of the Expected SR length
def SRExpectedLength(k):
    expectedvalue=0
    for x in range(0,int(math.ceil((2*k+1)/2))+1):
        for y in range(0, int(math.ceil((2*k+1)/2))+1 ):
            expectedvalue += (Probabilities(x,y,k) * SRExpectedDigit(x,y,k))
    return simplify(expectedvalue)


#This is the function which will return to you the equation of the expected length of a 2k+1 length game with Catch-Up Rules
#You enter in your k-value, for example k=1 for a 3-game series, and it will return to you the equation of the Expected CR length
def CRExpectedLength(k):
    expectedvalue=0
    for x in range(0,int(math.ceil((2*k+1)/2))+1):
        for y in range(0, int(math.ceil((2*k+1)/2))+1 ):
            expectedvalue += (Probabilities(x,y,k) * CRExpectedDigit(x,y,k))
    return simplify(expectedvalue)

########################################################################################################

#In this section we are actually running our list of values 'Values' through our expected length formulas and returning four arrays
#The first a 2D-array in which in each sub-array, we have the p and q value we entered into the function along with the corresponding expected length value that was returned, we do this for every combination of p and q in our 'Values list'
#The second through fourth items we are returning are a list of the p-values we entered, the list of q-values we entered, and a list of the expected lengths, all respectively

def SRReturningValues(k):
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every expected length value we get to two decimal points
            value = round(SRExpectedLength(k).subs([(p,Values[x]),(q,Values[y])]),2)
            #We append the values into their respective lists/arrays
            pvalues.append(Values[x])
            qvalues.append(Values[y])
            SRNewList.append([Values[x],Values[y],value])
            SREvalues.append(value)
    return SRNewList,pvalues,qvalues,SREvalues

def CRReturningValues(k):
    for x in range(0,len(Values)):
        for y in range(0,len(Values)):
            #Here we are rounding every expected length value we get to two decimal points
            value = round(CRExpectedLength(k).subs([(p,Values[x]),(q,Values[y])]),2)
            #We append the values into their respective lists/arrays
            pvalues.append(Values[x])
            qvalues.append(Values[y])
            CRNewList.append([Values[x],Values[y],value])
            CREvalues.append(value)
    return CRNewList,pvalues,qvalues,CREvalues

#######################################################################################################

#The SRMakeExcel and CRMakeExcel take in a value of k, and create, open, and fill an excel worksheet with a table of our
#p and q values for a best of 2k+1 game.
#Important to note that I decided not to automatically save/name the excel worksheet since the user may not want it automatically
#saved, and may just want to test it out or view the data. Thus, just made it such that user can alter the sheet/save themselves.

def SRMakeExcel(k):
    #Here we are setting the lists we are returning in SRReturningValues to variables
    SRNewList, pvalues, qvalues, SREvalues = SRReturningValues(k)
    #We are using xlwings to create and open an excel workbook
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    #Here we are filling our table with the data we recieve from our SRReturningValues function. Using a double for loop to
    #loop through each combination of p and q value and assign the corresponding expected length to it in the table
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = SREvalues[count]
            count = count+1
    #We are doing a for loop now to fill the labels/brackets of our table (placing the p and q values)
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    #Finally, we just want to add in a cell the 2k+1 series game for which we are calculating our data
    sht.cells(1,15).value = ("{}-game SR series").format((2*k)+1)

def CRMakeExcel(k):
    #Here we are setting the lists we are returning in CRReturningValues to variables
    CRNewList, pvalues2, qvalues2, CREvalues = CRReturningValues(k)
    #We are using xlwings to create and open an excel workbook
    wb = xw.Book()
    sht = wb.sheets('Sheet1')
    #Here we are filling our table with the data we recieve from our CRReturningValues function. Using a double for loop to
    #loop through each combination of p and q value and assign the corresponding expected length to it in the table
    count = 0
    for x in range(0,len(Values)):
        for y in range(0, len(Values)):
            sht.cells(2+y,2+x).value = CREvalues[count]
            count = count+1
    #We are doing a for loop now to fill the labels/brackets of our table (placing the p and q values)
    count = 0
    for x in range(0,len(Values)):
        sht.cells(2+x,1).value = Values[count]
        sht.cells(1,2+x).value = Values[count]
        count = count +1
    #Finally, we just want to add in a cell the 2k+1 series game for which we are calculating our data
    sht.cells(1,15).value = ("{}-game CR series").format((2*k)+1)

########################################################################################################

print(Probabilities(1,0,1))
#Finally, you are now able to create a brand new spreadsheet for any length game which will calculate all of the desired expected lengths for you
#You can do this by printing any of the MakeExcel functions
