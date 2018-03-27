#Shell - command line executor

import expr_classes
import expr_scanner
import expr_parser
import expr_execute
import expr_ilks
import expr_utilities
import expr_globals

#-----
# get next input from file
#-----
def getNextInputFromFile():
    thisReadfile = expr_globals.rf_ReadfileList
    if (thisReadfile == 0):
        return 0
    fileLine = thisReadfile.getLine()
    #if we were at the end of the file, pop file stack, and return ""
    if (fileLine == 0):
        expr_utilities.printDebug( "Reached EOF for " + thisReadfile.getName() )
        expr_globals.rf_ReadfileList = thisReadfile.getNext()
        return ""
    return fileLine
    
#--------------------- 
# the main function
#---------------------
def sh( inputLine=0 ):

    expr_globals.init()
    
    if (inputLine != 0 and inputLine != ""):
        #mainly for debugging; sh() should ordinarily not be called w/ arg
        shell( inputLine, 1 )
        return

    # interactive shell
    while( expr_globals.n_ExitFlag == 0 ):
        # get next line of input to execute
        if (expr_globals.rf_ReadfileList != 0):
            userInput = getNextInputFromFile()
        else:
            userInput = input( expr_globals.sz_ShellPrompt )
        
        if (userInput != ""):
            expr_globals.n_ErrorSeen = 0            
            firstToken = expr_scanner.makeTokenList( userInput )
            if (expr_globals.n_ErrorSeen != 0):
                print( "***** sh(): Syntax Error *****" )
            else:
                expr_execute.executeCommand( firstToken )
                
    #return, possibly to continuation of a method execution
    expr_globals.n_ExitFlag = 0
    return


#--------
# shell() - assumes program already initialized, and a non-zero input line
#--------
def shell( inputLine, nInitialized=0 ):
    if (nInitialized == 0):
        expr_globals.init()
    if (inputLine == 0):
        return 0
    if (inputLine == ""):
        return ""

    
    #save the old context, and make a new one for this shell execution
    nErrorSeenSav = expr_globals.n_ErrorSeen
    expr_globals.n_ErrorSeen = 0
    tCurTokenSav = expr_globals.t_CurToken
    expr_globals.t_CurToken = 0
    rfReadfileListSav = expr_globals.rf_ReadfileList
    expr_globals.rf_ReadfileList = 0
    nExitFlagSav = expr_globals.n_ExitFlag
    expr_globals.n_ExitFlag = 0
    
    #tokenize and execute the line of text that was passed in
    firstToken = expr_scanner.makeTokenList( inputLine )
    if (expr_globals.n_ErrorSeen == 0):
        expr_execute.executeCommand( firstToken )

    #The command might have been to read a file. If so, we must process all
    #lines in the file (which in turn could have us read another file, etc.)
    inputLine = getNextInputFromFile()
    while (inputLine != 0):
        if (inputLine != ""):
            expr_globals.n_ErrorSeen = 0            
            firstToken = expr_scanner.makeTokenList( inputLine )
            if (expr_globals.n_ErrorSeen != 0):
                print( "***** shell(): Syntax Error *****" )
            else:
                expr_execute.executeCommand( firstToken )
        inputLine = getNextInputFromFile()

    #restore the original context
    expr_globals.n_ErrorSeen = nErrorSeenSav
    expr_globals.t_CurToken = tCurTokenSav
    expr_globals.rf_ReadfileList = rfReadfileListSav
    expr_globals.n_ExitFlag = nExitFlagSav

