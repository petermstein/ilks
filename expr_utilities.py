#Utilities for expression analyzer

import expr_globals
import expr_classes

#--------------------- 
# debug() - different levels of debug
#---------------------
def printDebug(a):
    if (expr_globals.n_Debug != 0):
        print("DEBUG:", a)

#--------------------- 
# printError() - set error flag, print msg
#---------------------
def printError( functionName, errorMsg ):
    print( functionName, ": ERROR: ", errorMsg, sep="" )
    expr_globals.n_ErrorSeen = 1

#--------------------- 
# getVarFromName() - return variable object, given its name
#---------------------
def getVarFromName( name ):
    curVar = expr_globals.v_VarList
    while( curVar != 0):
        if (curVar.getName() == name ):
            break
        curVar = curVar.getNext()
    return curVar

#--------------------- 
# setVar() - set a variable to a value
#---------------------
def setVar( szName, szType, value ):
    curVar = getVarFromName( szName )
    if (curVar == 0):
        newVar = expr_classes.Var( szName, szType, value )
        newVar.pointTo( expr_globals.v_VarList )
        expr_globals.v_VarList = newVar
    else:
        curVar.setValue( value )

#--------------------- 
# showVarList() - print out a list of vars
#---------------------
def showVarList( vVarList ):
    curVar = vVarList
    while (curVar != 0):
        print( curVar.getName(), "=", curVar.getValue(), "(type=", curVar.getType(), ")" )
        curVar = curVar.getNext()

#--------------------- 
# showIlkList() - print out a list of ilks
#---------------------
def showIlkList( iIlkList ):
    curIlk = iIlkList
    while (curIlk != 0):
        print( curIlk.getName() )
        curIlk = curIlk.getNext()
