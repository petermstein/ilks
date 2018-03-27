#Execute functions for expression alanyzer

import expr_classes
import expr_utilities
import expr_globals
import expr_parser
import expr_ilks


#-----
# give help
#-----
def giveHelp( n ):
    if (n==1 or n==2):
        #eventually give more detailed help for n==2
        print( "+-----------------" )
        print( "| This is a command line executor." )
        print( "| The list of commands is as follows:" )
        print( "|   - help (show this message)" )
        print( "|   - Help (show longer help message)" )
        print( "|   - eval <mathematical expression> (can set vars in middle)" )
        print( "|   - setvar <name> <value>" )
        print( "|   - showvars (prints out a list of variables & their values)" )
        print( "|   - showilks (prints out a list of ilks' names)" )
        print( "|   - readfile <filename> (executes commands in a file)" )
        print( "|   - echo (echoes the rest of the line)" )
        print( "|   - setprompt <new_prompt> (set your own prompt)" )
        print( "|   - shell <string> (executes command in new shell)" )
        print( "|   - exit (causes the program to end)" )
        print( "|       [---ilk stuff below---]" )
        print( "|   - readilkfile <filename> (gathers ilk definitions)" )
        print( "|   - makeobject <obj_type> <obj_name> <args if any>" )
        print( "|   - sendobject <obj_type> <obj_name> <message> <args if any>" )
        print( "+-----------------" )
    elif (n==3):
        print( "+-----------------" )
        print( "|   - debug" )
        print( "|   - nodebug" )
        print( "|   - parseerror" )
        print( "|   - noparseerror" )
        print( "|   - parsetree" )
        print( "|   - noparsetree" )
        print( "|   - showopenfiles" )
        print( "|   - help" )
        print( "|   - Help" )
        print( "|   - HELP" )
        print( "|   - HelP" )
        print( "|   - setvar" )
        print( "|   - showvars" )
        print( "|   - showilks" )
        print( "|   - readfile" )
        print( "|   - readilkfile" )
        print( "|   - setprompt" )
        print( "|   - echo" )
        print( "|   - shell" )
        print( "|   - exit" )
        print( "+-----------------" )
        
#eventually have a separate, more elaborate help for n=2

#------
# executeCommnad()
#------
def executeCommand( firstToken ):
    expr_utilities.printDebug("In executeCommand" )
    if (firstToken == 0):
        return

    if (firstToken.getType() == "alphanum" ):
        szThisCommand = firstToken.getValue()
        if (szThisCommand == "debug"):
            print( "Turning debug on" )
            expr_globals.n_Debug = 1
        elif (szThisCommand == "nodebug"):
            print( "Turning debug off" )
            expr_globals.n_Debug = 0
        elif (szThisCommand == "parseerror"):
            expr_globals.n_ErrorSeen = 1
        elif (szThisCommand == "noparseerror"):
            expr_globals.n_ErrorSeen = 0
        elif (szThisCommand == "parsetree" ):
            print( "Turning parsetree display on" )
            expr_globals.n_DisplayParsetree = 1
        elif (szThisCommand == "noparsetree" ):
            print( "Turning parsetree display off" )
            expr_globals.n_DisplayParsetree = 0
        elif (szThisCommand == "showopenfiles"):
            print( "---vv---open-files---vv---" )
            curOpenFile=expr_globals.rf_ReadfileList
            while( curOpenFile != 0 ):
                print( "openfile:", curOpenFile.getName() )
                curOpenFile = curOpenFile.getNext()
            print( "---^^---open-files---^^---" )
        elif (szThisCommand == "help"):
            giveHelp( 1 )
        elif (szThisCommand == "Help"):
            giveHelp( 2 )
        elif (szThisCommand == "HELP"):
            giveHelp( 3 )
        elif (szThisCommand == "HelP"):
            print ( "{debug, nodebug, parseerror, parsetree, noparsetree, help, Help, HelP, showopenfiles}" )
        elif (szThisCommand == "setvar" ):
            expr_parser.evalSetVar( firstToken.getNext() )
        elif (szThisCommand == "showvars" ):
            print( "---vv---variables---vv---" )
            expr_utilities.showVarList( expr_globals.v_VarList )
            print( "---^^---variables---^^---" )
        elif (szThisCommand == "showilks" ):
            print( "---vv---ilks---vv---" )
            expr_utilities.showIlkList( expr_globals.i_IlkList )
            print( "---^^---ilks---^^---" )
        elif (szThisCommand == "eval"):
            mathValue = expr_parser.evalEval( firstToken.getNext() )
            print( mathValue )
        elif (szThisCommand == "readfile"):
            expr_parser.evalOpenReadfile( firstToken.getNext() )
        elif (szThisCommand == "readilkfile"):
            expr_parser.evalReadIlkfile( firstToken.getNext() )
        elif (szThisCommand == "setprompt"):
            expr_parser.evalSetPrompt( firstToken.getNext() )
        elif (szThisCommand == "echo"):
            expr_parser.evalEcho( firstToken.getNext() )
        elif (szThisCommand == "shell"):
            expr_parser.evalShell( firstToken.getNext() )
        elif (szThisCommand == "exit"):
            expr_globals.n_ExitFlag = 1
        else:
            print( "Unknown command:", szThisCommand )
        return

    if (firstToken.getType() == "number" ):
        print( "Temp: Number command:", firstToken.getValue() )
        return

#-----
# display parse tree
#-----
def displayMathParsetree( ptParsetree, n ):
    if (ptParsetree == 0):
        print( "<displayMathParsetree:  NULL PARSE TREE>")
    else:
        print( "| ", ' '*n*2, sep="", end="" )
        print( ptParsetree.getType(), " ... ", ptParsetree.getValue(), sep="" )
        if ( ptParsetree.getChild1() != 0 ):
            displayMathParsetree( ptParsetree.getChild1(), n+1 )
            if (ptParsetree.getChild2() != 0 ):
                displayMathParsetree( ptParsetree.getChild2(), n+1 )

#-----
# execute parse tree
#-----
def executeMathParsetree( thisParsetree ):
    if (thisParsetree == 0):
        return 0

    #possible types are: {number, mathop, varialbe, setvariable}
    if (thisParsetree.getType() == "number"):
        expr_utilities.printDebug( "executeMathParsetree: returning a number: " + str(thisParsetree.getValue()))
        return thisParsetree.getValue()

    if (thisParsetree.getType() == "mathop"):
        expr_utilities.printDebug( "executeMathParsetree: returning result of mathop: " + thisParsetree.getValue())
        if (thisParsetree.getValue() == "+"):
            return( executeMathParsetree(thisParsetree.getChild1()) + executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "-"):
            return( executeMathParsetree(thisParsetree.getChild1()) - executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "*"):
            return( executeMathParsetree(thisParsetree.getChild1()) * executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "/"):
            return( executeMathParsetree(thisParsetree.getChild1()) / executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "~"):
            return(( executeMathParsetree(thisParsetree.getChild1()) + executeMathParsetree(thisParsetree.getChild2()))/2)
        if (thisParsetree.getValue() == "^"):
            return( executeMathParsetree(thisParsetree.getChild1()) ** executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "%"):
            return( executeMathParsetree(thisParsetree.getChild1()) % executeMathParsetree(thisParsetree.getChild2()))
        if (thisParsetree.getValue() == "`"):
            return( executeMathParsetree(thisParsetree.getChild1()) // executeMathParsetree(thisParsetree.getChild2()))
        
    if (thisParsetree.getType() == "compare"):
        expr_utilities.printDebug( "executeMathParsetree: returning result of comparison: " + thisParsetree.getValue())
        child1value = executeMathParsetree(thisParsetree.getChild1())
        child2value = executeMathParsetree(thisParsetree.getChild2())
        if (thisParsetree.getValue() == "eq"):
            if child1value == child2value:
                return 1
            return 0
        if (thisParsetree.getValue() == "ne"):
            if child1value != child2value:
                return 1
            return 0
        if (thisParsetree.getValue() == "lt"):
            if child1value < child2value:
                return 1
            return 0
        if (thisParsetree.getValue() == "gt"):
            if child1value > child2value:
                return 1
            return 0
        if (thisParsetree.getValue() == "le"):
            if child1value <= child2value:
                return 1
            return 0
        if (thisParsetree.getValue() == "ge"):
            if child1value >= child2value:
                return 1
            return 0

    if (thisParsetree.getType() == "variable"):
        expr_utilities.printDebug( "executeMathParsetree: returning value of variable: " + thisParsetree.getValue())
        thisVar = expr_utilities.getVarFromName( thisParsetree.getValue() )
        if (thisVar == 0):
            expr_utilities.printError( "executeMathParsetree", "No such varable: " + thisParsetree.getValue() )
            return 0
        if thisVar.getType() == "number":
            return thisVar.getValue()
        else:
            return 0

    if (thisParsetree.getType() == "setvariable"):
        valueToSet = executeMathParsetree( thisParsetree.getChild1() )
        expr_utilities.printDebug( "executeMathParsetree: returning setting of variable " + thisParsetree.getValue() + " to " + str(valueToSet) )
        expr_utilities.setVar( thisParsetree.getValue(), "number", valueToSet )
        return valueToSet

    expr_utilities.printDebug( executeMathParsetree, "Unknown parsetree type, value: " + thisParsetree.getType() + ", " + thisParsetree.getValue())
    return 0
