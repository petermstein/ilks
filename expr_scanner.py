#Scanner functions for expression alanyzer

import expr_classes
import expr_utilities
import expr_globals

#---------------------
# various helper functions
#---------------------
def isNumber( char ):
    if( char >= '0' and char <= '9' ):
        return 1
    else:
        return 0
    
def isLetter( char ):
    if ((char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z')):
        return 1
    else:
        return 0

def isWhiteSpace( char ):
    if (char == ' ' or char =='\t' or char == '\n'):
        return 1
    else:
        return 0

def scanPastWhiteSpaceAndComments( userInput, i, inputLength ):
    while (i < inputLength ):
        nWhiteSpaceSeen = 0
        nCommentSeen = 0

        #get past white space if any
        if (isWhiteSpace( userInput[i] )):
            nWhiteSpaceSeen = 1
            i = i+1
            while (i < inputLength and isWhiteSpace( userInput[i] )):
                i = i+1

        #get past comment if any
        if (i < (inputLength-1) and userInput[i]=='/' and userInput[i+1]=='*'):
            nCommentSeen = 1
            #comment started, get to the end of it
            i = i + 2
            while( i < (inputLength-1) ):
                if (userInput[i]=='*' and userInput[i+1]=='/'):
                    i = i+2
                    break
                i = i+1

        if nWhiteSpaceSeen == 0 and nCommentSeen == 0:
            break

    return i

#---------------------
# token maker function - makeNumberToken()
#---------------------
def makeNumberToken(userInput, i, inputLength):
    if (i >= inputLength ):
        expr_utilities.printError( "makeNumberToken", "Called on end of string")
        return 0

    thisChar = userInput[i]
    if (isNumber(thisChar) == 0 and thisChar != '.'):
        expr_utilities.printError( "makeNumberToken", "First character not a number or decimal point")
        return 0
    decimalPoint = 0
    numAsString = ""
    while( isNumber(thisChar) or thisChar == "." ):
        if thisChar == ".":
            if (decimalPoint == 1):
                break
            decimalPoint = 1
        numAsString = numAsString + thisChar
        i = i + 1
        if (i == inputLength):
            break
        thisChar = userInput[i]
    if (decimalPoint == 1):
        thisNumber = float( numAsString )
    else:
        thisNumber = int( numAsString )
        
#    while( isNumber(thisChar)):
#        thisNumber = (10*thisNumber) + (ord(thisChar)-ord('0'))
#        i = i + 1
#        if (i == inputLength):
#            break
#        thisChar = userInput[i]


    #now the number gathered up is stored
    return expr_classes.Token("number", thisNumber ), i

#---------------------
# token maker function - makeAlphanumToken()
#---------------------       
def makeAlphanumToken(userInput, i, inputLength):
    if (i >= inputLength ):
        expr_utilities.printError( "makeAlphanumToken", "Called on end of string")
        return 0

    alphanumBeginPosition = i
    thisChar = userInput[i]
    if (isLetter(thisChar) == 0):
        expr_utilities.printError( "makeAlphanumToken", "First character not a letter")
        return 0

    while( isLetter(thisChar) or isNumber(thisChar) or thisChar == '_' or thisChar == '.'):
        i=i+1
        if i == inputLength:
            break
        thisChar = userInput[i]

    thisAlphanum = userInput[alphanumBeginPosition:i]
    return expr_classes.Token("alphanum", thisAlphanum ), i

#--------------------- 
# makeNextToken() - lexical analyzer that returns tokens based on input
#---------------------
def makeNextToken( userInput, i, inputLength ):
    if (i >= inputLength):
        expr_utilities.printError( "makeNextToken", "Called on end of string" )
        return 0, i

    i = scanPastWhiteSpaceAndComments( userInput, i, inputLength )
    if (i >= inputLength ):
        expr_utilities.printDebug("makeNextToken: string ended in white space or comment" )
        return 0, i
    
    thisChar = userInput[i]
    tokenToReturn = 0

    #see if it's a number - could start w/ digit or '.' (e.g., .1)
    numberFlag = 0
    if (isNumber( thisChar )):
        numberFlag = 1
    elif (thisChar == '.'):
        j = i+1
        if (j < inputLength and isNumber( userInput[j] ) ):
            numberFlag = 1

    #number token
    if (numberFlag == 1):
        tokenToReturn, i = makeNumberToken( userInput, i, inputLength )

    #alphanum token
    elif isLetter( thisChar ):
        tokenToReturn, i = makeAlphanumToken( userInput, i, inputLength )

    #paren tokens
    elif (thisChar == '(' or thisChar == '['):
        i = i + 1
        tokenToReturn = expr_classes.Token( "lparen", thisChar )
    elif (thisChar == ')' or thisChar == ']'):
        i = i + 1
        tokenToReturn = expr_classes.Token( "rparen", thisChar )

    #string token
    elif (thisChar == '"'):
        gatherString = ""
        endQuoteFlag = 0
        i = i + 1
        while( i < inputLength ):
            nextChar = userInput[i]
            if (nextChar == '"'):
                endQuoteFlag = 1
                i = i + 1
                break
            gatherString = gatherString + nextChar
            i = i + 1
        if endQuoteFlag == 0:
            expr_utilities.printError( "makeNextToken", "No end quote for string" )
        tokenToReturn = expr_classes.Token( "string", gatherString )

    #numerical comparisons
    elif (thisChar == '=' and i<(inputLength-1) and userInput[i+1] == '='):
        i = i + 2
        tokenToReturn = expr_classes.Token( "compare", "eq" )
    elif (thisChar == '!' and i<(inputLength-1) and userInput[i+1] == '='):
        i = i + 2
        tokenToReturn = expr_classes.Token( "compare", "ne" )
    elif (thisChar == '<' and i<(inputLength-1) and userInput[i+1] == '='):
        i = i + 2
        tokenToReturn = expr_classes.Token( "compare", "le" )
    elif (thisChar == '>' and i<(inputLength-1) and userInput[i+1] == '='):
        i = i + 2
        tokenToReturn = expr_classes.Token( "compare", "ge" )
    elif (thisChar == '<'):
        i = i + 1
        tokenToReturn = expr_classes.Token( "compare", "lt" )
    elif (thisChar == '>'):
        i = i + 1
        tokenToReturn = expr_classes.Token( "compare", "gt" )

    #default case
    else:
        i = i + 1
        if (thisChar == '*' and (i < inputLength) and userInput[i] == '*'):
            i = i + 1
            thisChar = '^'
        elif (thisChar == '/' and (i < inputLength) and userInput[i] == '/'):
            i = i + 1
            thisChar = '`'
        tokenToReturn = expr_classes.Token( "other", thisChar )
    return( tokenToReturn, i )

#--------------------- 
# makeTokenList() - put the structure together based on tokens returned from lexical analyzer
#---------------------
def makeTokenList( userInput ):    
    inputLength = len( userInput )
    i = 0
    firstToken = 0
    lastToken = 0
    while( i < inputLength ):
        #get the next token from the input
        thisToken, i = makeNextToken( userInput, i, inputLength )
        if thisToken == 0:
            expr_utilities.printDebug( "makeTokenList: null token received" )
        else:
            expr_utilities.printDebug( "makeTokenList: token type, value: " + thisToken.getType() + ", " + str(thisToken.getValue()) )
            if firstToken == 0:
                firstToken = thisToken
            if lastToken != 0:
                lastToken.pointTo( thisToken )
                thisToken.pointBackTo( lastToken )
            lastToken = thisToken
    return firstToken  #, lastToken
            
