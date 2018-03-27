#Parser functions for expression alanyzer

import expr_classes
import expr_utilities
import expr_globals
import expr_main
import expr_execute
import expr_ilks
import expr_scanner

#-----
# evalOpenReadfile - evaluate a read-file command
#-----
def evalOpenReadfile( readfileToken ):
    if (readfileToken == 0):
        expr_utilities.printError( "evalOpenReadfile", "No file name supplied" )
        return
    if (readfileToken.getType() != "alphanum" ):
        expr_utilities.printError( "evalOpenReadfile", "File name not an alphanum" )
        return
    szReadfileName = readfileToken.getValue()
    if (readfileIsOpen( szReadfileName )):
        print( "WARNING: evalOpenReadfile: File (", szReadfileName, ") is open, cannot open it again.", sep="" )
        return
    #open file, put on top of stack
    try:
        expr_utilities.printDebug( "Opening readfile " + szReadfileName )
        foThisFileObject = open( szReadfileName )
        #make new Readfile, gather up input from it
        rfThisReadfile = expr_classes.Readfile( szReadfileName )
        rfThisReadfile.gatherInput( foThisFileObject )
        foThisFileObject.close()
        #push it onto the stack of readfiles
        rfThisReadfile.pointTo( expr_globals.rf_ReadfileList )
        expr_globals.rf_ReadfileList = rfThisReadfile        
    except IOError:
        print( "ERROR: evalOpenReadfile: IOError: Cannot open file:", szReadfileName )

def readfileIsOpen( name ):
    curReadfile = expr_globals.rf_ReadfileList
    while( curReadfile != 0 ):
        if curReadfile.getName() == name:
            return( 1 )
        curReadfile = curReadfile.getNext()
    return( 0 )

#-----
# evalReadIlkfile - evaluate a read-file command
#-----
def evalReadIlkfile( ilkfileToken ):
    if (ilkfileToken == 0):
        expr_utilities.printError( "ReadIlkfile", "No file name supplied" )
        return
    if (ilkfileToken.getType() != "alphanum" ):
        expr_utilities.printError( "ReadIlkfile", "File name not an alphanum" )
        return
    ilkfileContents = expr_ilks.readIlkfile( ilkfileToken )
    if (ilkfileContents == 0):
        return
    print( "---vv---ilkfile-contents---vv---" )
    print( ilkfileContents )
    print( "---^^---ilkfile-contents---^^---" )
    expr_globals.n_ErrorSeen = 0
    ilkTokenlist = expr_scanner.makeTokenList( ilkfileContents )
    if expr_globals.n_ErrorSeen == 0:
        ilkVarlist, ilkMethodlist = expr_ilks.ParseIlkTokens( ilkTokenlist )
        if (expr_globals.n_ErrorSeen != 0):
            return 0
        #make the new ilk and add it to the list of ilks
        newIlk = expr_classes.Ilk( ilkTokenlist, ilkVarlist, ilkMethodlist )
        newIlk.pointTo( expr_globals.i_IlkList )
        expr_globals.i_IlkList = newIlk
        if (expr_globals.n_DisplayParsetree != 0):
            print( "+-----" )
            expr_ilks.displayIlk( newIlk )
            print( "+-----" )

    
#-----
# evalSetVar - evaluate a set-variable command
#-----
def evalSetVar( nameToken ):
    if (nameToken == 0):
        expr_utilities.printError( "evalSetVar", "No variable name supplied" )
        return
    valueToken = nameToken.getNext()
    if (valueToken == 0):
        expr_utilities.printError( "evalSetVar", "No variable value supplied" )
        return
    if (nameToken.getType() != "alphanum" ):
        expr_utilities.printError( "evalSetVar", "Var name not an alphanum" )
        return
    if (valueToken.getType() != "number" and valueToken.getType() != "string"):
        expr_utilities.printError( "evalSetVar", "Var value not number or string" )
        return
    expr_utilities.setVar( nameToken.getValue(), valueToken.getType(), valueToken.getValue() )

#-----
# evalEval - evaluate an eval command, return expression's value
#-----
def evalEval( evalToken ):
    expr_globals.t_CurToken = evalToken
    mathParsetree = makeMathParsetree()
    if( expr_globals.n_ErrorSeen != 0):
        print( "***** Parse Error *****")
        return( 0 )
    if (expr_globals.n_DisplayParsetree != 0):
        print( "+-----" )
        expr_execute.displayMathParsetree( mathParsetree, 0 )
        print( "+-----" )
    return( expr_execute.executeMathParsetree( mathParsetree ) )
    
#-----
# evalSetPrompt - evaluate a set-prompt command
#-----
def evalSetPrompt( promptToken ):
    if (promptToken == 0):
        expr_utilities.printError( "evalSetPrompt", "No new prompt supplied" )
        return
    expr_globals.sz_ShellPrompt = promptToken.getValue() + " "

#-----
# evalEcho - evaluate an echo command
#-----
def evalEcho( echoToken ):
    #gather up and print the output
    output = ""
    while( echoToken != 0):
        output = output + str( echoToken.getValue() )
        echoToken = echoToken.getNext()
        if (echoToken != 0):
            output = output + " "
    print( output )

#-----
# evalShell - evaluate a shell command
#-----
def evalShell( shellToken ):
    if (shellToken == 0):
        expr_utilities.printError( "evalShell", "No command supplied" )
        return
    if( shellToken.getType() != "string"):
        expr_utilities.printError( "evalShell", "Non-string command supplied" )
        return
    expr_main.shell( shellToken.getValue() )


#-----
# make math parse tree
#  assumes the global cur token has been set to the start token
#    this is called from the shell, as well as from the ilk method parser
#-----
def makeMathParsetree():
    expr_utilities.printDebug( "In makeMathParsetree")
    #-------------------------------------
    #<S> : <E0> <COMPARE> <S> | <E0>
    #<E0>: VAR "=" <E1> | <E1>
    #<E1>: <E2> "+" <E1> | <E2> "-" <E1> | <E2>
    #<E2>: <E3> "*" <E2> | <E3> "/" <E2> | <E3> "~" <E2> |<E3>
    #<E3>: <E4> "^" <E3> | <E4> "%" <E3> | <E4>
    #<E4>: "(" <S> ")" | VAR | NUM | "(" ")"
    #COMPARE: "==" | "!=" | ">=" | "<=" | ">" | "<"
    #-------------------------------------
    return parseS()

#-----
# parse an S expression
# <S>: <E0> <COMPARE> <S> | <E0>
#-----
def parseS():
    expr_utilities.printDebug( "In parseS()" )
    #assumes expr_globals.t_CurToken is set to the next token to parse, both before and after the call to parseE0()
    e0Node = parseE0()
    firstToken = expr_globals.t_CurToken
    if (firstToken != 0 and firstToken.getType() == "compare"):
        expr_utilities.printDebug( "ES: Saw a compare, namely " + firstToken.getValue() )
        expr_globals.t_CurToken = firstToken.getNext()
        SNode = parseS()  #calls self recursively
        newNode = expr_classes.Node( "compare", firstToken.getValue() )
        newNode.pointToAsChild1( e0Node )
        newNode.pointToAsChild2( SNode )
        return( newNode )
    return e0Node

#-----
# parse a start-state expression
# <E0> : VAR "=" <E1> | <E1>
#-----
def parseE0():
    expr_utilities.printDebug( "In parseE0()" )
    firstToken = expr_globals.t_CurToken
    if (firstToken == 0):
        return 0
    secondToken = firstToken.getNext()
    if (firstToken.getType() == "alphanum" and secondToken != 0 and secondToken.getValue() == "=" and secondToken.getNext() != 0):
        expr_globals.t_CurToken = secondToken.getNext()
        returnTree = expr_classes.Node( "setvariable", firstToken.getValue() )
        returnTree.pointToAsChild1( parseE1() )
        return( returnTree )
    return( parseE1() )

#-----
# parse an E1 expression
# <E1>: <E2> "+" <E1> | <E2> "-" <E1> | <E2>
#-----
def parseE1():
    expr_utilities.printDebug( "In parseE1()" )
    #assumes expr_globals.t_CurToken is set to the next token to parse, both before and after the call to parseE2()
    e2Node = parseE2()
    firstToken = expr_globals.t_CurToken
    if (firstToken != 0 and firstToken.getType() == "other" and (firstToken.getValue() == "+" or firstToken.getValue() == "-")):
        expr_utilities.printDebug( "E1: Saw a plus or minus of type " + firstToken.getValue() )
        expr_globals.t_CurToken = firstToken.getNext()
        e1Node = parseE1()  #calls self recursively
        newNode = expr_classes.Node( "mathop", firstToken.getValue() )
        newNode.pointToAsChild1( e2Node )
        newNode.pointToAsChild2( e1Node )
        return( newNode )
    return e2Node

#-----
# parse an E2 expression
# <E2>: <E3> "*" <E2> | <E3> "/" <E2> | <E3> "~" <E2> |<E3>
#-----
def parseE2():
    expr_utilities.printDebug( "In parseE2()" )
    #assumes expr_globals.t_CurToken is set to the next token to parse, both before and after the call to parseE3()
    e3Node = parseE3()
    firstToken = expr_globals.t_CurToken
    if (firstToken != 0 and firstToken.getType() == "other" and (firstToken.getValue() == "*" or firstToken.getValue() == "/" or firstToken.getValue() == "~")):
        expr_utilities.printDebug( "E2: Saw a times or divided-by or avg of type " + firstToken.getValue() )
        expr_globals.t_CurToken = firstToken.getNext()
        e2Node = parseE2()  #calls self recursively
        newNode = expr_classes.Node( "mathop", firstToken.getValue() )
        newNode.pointToAsChild1( e3Node )
        newNode.pointToAsChild2( e2Node )
        return( newNode )
    else:
        return e3Node

#-----
# parse an E3 expression
# <E3>: <E4> "^" <E3> | <E4> "%" <E3> | <E4>
#-----
def parseE3():
    expr_utilities.printDebug( "In parseE3()" )
    #assumes expr_globals.t_CurToken is set to the next token to parse, both before and after the call to parseE4()
    e4Node = parseE4()
    firstToken = expr_globals.t_CurToken
    if (firstToken != 0 and firstToken.getType() == "other" and (firstToken.getValue() == "^" or firstToken.getValue() == "%" or firstToken.getValue() == "`")):
        expr_utilities.printDebug( "E3: Saw a power or modulo of type " + firstToken.getValue() )
        expr_globals.t_CurToken = firstToken.getNext()
        e3Node = parseE3()  #calls self recursively
        newNode = expr_classes.Node( "mathop", firstToken.getValue() )
        newNode.pointToAsChild1( e4Node )
        newNode.pointToAsChild2( e3Node )
        return( newNode )
    else:
        return e4Node

#-----
# pares an E4 expression
# <E4>: "(" <S> ")" | VAR | NUM | "(" ")"
#-----
def parseE4():
    expr_utilities.printDebug( "In parseE4()" )
    firstToken = expr_globals.t_CurToken
    if (firstToken == 0):
        expr_utilities.printError( "parseE4", "Null first token" )
        return 0

    if (firstToken.getType() == "lparen"):
        expr_utilities.printDebug( "E4: saw a left paren" )
        #move past the left paren
        expr_globals.t_CurToken = firstToken.getNext()

        #see if it's a null expression w/in the parens, if so return a number-0 node
        if (expr_globals.t_CurToken.getType() == "rparen"):
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
            expr_utilities.printDebug( "E4: saw null expr w/in parens: using 0" )
            numberNode = expr_classes.Node( "number", 0 )
            return numberNode
            
        #make an S parse tree out of stuff between parens
        SNode = parseS()
        #see what the next token is after making the E1 parse tree
        firstToken = expr_globals.t_CurToken
        if (firstToken == 0):
            expr_utilities.printError( "parseE4", "Closing paren not found: null next token" )
        elif (firstToken.getType() != "rparen" ):
            expr_utilities.printError( "parseE4", "Closing paren not found: next token of type & value: " + firstToken.getType() + ", " + str(firstToken.getValue()) )
        else:
            expr_utilities.printDebug( "E4: saw a right paren" )
            #move past the right paren
            expr_globals.t_CurToken = firstToken.getNext()
        return SNode

    # move the global pointer up
    expr_globals.t_CurToken = firstToken.getNext()
    
    if (firstToken.getType() == "alphanum"):
        expr_utilities.printDebug( "E4: saw a variable name" )
        varNode = expr_classes.Node( "variable", firstToken.getValue() )
        return varNode

    if (firstToken.getType() == "number"):
        expr_utilities.printDebug( "E4: saw a number" )
        numberNode = expr_classes.Node( "number", firstToken.getValue() )
        return numberNode

    if (firstToken.getType() == "other" and firstToken.getValue() == "-"):
        secondToken = firstToken.getNext()
        if (secondToken == 0):
            expr_utilities.printError( "parseE4", "Minus sign seen at end of token list" )
            return 0
        if (secondToken.getType() == "number"):
            #move the global pointer up one more
            expr_globals.t_CurToken = secondToken.getNext()
            expr_utilities.printDebug( "E4: saw a negative number" )
            numberNode = expr_classes.Node( "number", 0-secondToken.getValue() )
            return numberNode
        else:
            expr_utilities.printError( "parseE4", "Expected number after minus sign" )
            return 0

    expr_utilities.printError( "parseE4", "Unknown first node, of type: " + firstToken.getType())
    return 0
