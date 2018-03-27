#Ilk functions for command line executor

import expr_classes
import expr_utilities
import expr_globals
import expr_parser


#-----
# some small utilities
#-----
def isAlphanum( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "alphanum"):
        return 1
    return 0
def isParticAlphanum( thisToken, szValue ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "alphanum" and thisToken.getValue() == szValue ):
        return 1
    return 0
def isLcurly( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "other" and thisToken.getValue() == "{"):
        return 1
    return 0
def isRcurly( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "other" and thisToken.getValue() == "}"):
        return 1
    return 0
def isLparen( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "lparen"):
        return 1
    return 0
def isRparen( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "rparen"):
        return 1
    return 0
def isSemi( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "other" and thisToken.getValue() == ";"):
        return 1
    return 0
def isComma( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "other" and thisToken.getValue() == ","):
        return 1
    return 0
def isEqualSign( thisToken ):
    if thisToken == 0:
        return 0
    if (thisToken.getType() == "other" and thisToken.getValue() == "="):
        return 1
    return 0

#-----
# display ilk parse tree
#-----
def displayIlk( iThisIlk ):
    if (iThisIlk == 0):
        print( "<displayIlk:  NULL ILK>")
        return
    print( "| Contents of ilk '", iThisIlk.getName(), "'", sep="" )
    print( "+---- ilk vars --------------------------")
    displayIlkVarlist( iThisIlk.getVarlist() )
    print( "+---- ilk methods --------------------------")
    displayIlkMethodlist( iThisIlk.getMethodlist() )
#---------------------------------------------------
def displayIlkVarlist( vVarlist ):
    if (vVarlist == 0):
        print( "|  (None)" )
    while (vVarlist != 0):
        if (vVarlist.getType() == "number" ):
            print( "| var:", vVarlist.getType(), vVarlist.getName(), "=", vVarlist.getValue() )
        else:
            print( "| var: ", vVarlist.getType(), " ", vVarlist.getName(), " = '", vVarlist.getValue(), "'", sep="" )
        vVarlist = vVarlist.getNext()
    return
#---------------------------------------------------
def displayIlkMethodlist( mMethodlist ):
    if (mMethodlist == 0):
        print( "|  (None) [should never happen]" )
    mThisMethod = mMethodlist
    while( mThisMethod != 0 ):
        print( "| ...............................")
        print( "| .... method:", mThisMethod.getName() )
        print( "| ...............................")
        vThisArg = mThisMethod.getArgs()
        print( "| args:" )
        if (vThisArg == 0):
            print( "|  (None)" )
        while (vThisArg != 0 ):
            print( "| ", vThisArg.getType(), vThisArg.getName(), "=", vThisArg.getValue() )
            vThisArg = vThisArg.getNext()
        displayMethodTree( mThisMethod.getTree() )
        mThisMethod = mThisMethod.getNext()
    return
#---------------------------------------------------
def displayMethodTree( pnMethodTree ):
    pnThisMethodStmt = pnMethodTree
    if (pnThisMethodStmt == 0):
        print( "|  (No statments in the method)" )
        return
    while (pnThisMethodStmt != 0):
        displayMethodStmt( pnThisMethodStmt, 0 )
        pnThisMethodStmt = pnThisMethodStmt.getNext()
#---------------------------------------------------
def displayMethodStmt( pnThisMethodStmt, n ):
    if (pnThisMethodStmt == 0):
        return
    szStmtType = pnThisMethodStmt.getType()
    print( "| ", ' '*n*2, "stmt-type='", szStmtType, "'", sep="" )
    if (szStmtType == "shell"):
        displayMethodStmtShell( n, pnThisMethodStmt.getValue() )
    elif (szStmtType == "setnumber" ):
        displayMethodStmtSetnumber( n, pnThisMethodStmt.getValue(), pnThisMethodStmt.getChild1() )
    elif (szStmtType == "setstring" ):
        displayMethodStmtSetstring( n, pnThisMethodStmt.getValue(), pnThisMethodStmt.getChild1() )
#---------------------------------------------------
def displayMethodStmtShell( n, szStmtValue ):
    print( "| ", ' '*((n*2)+2), "shell cmd='", szStmtValue, "'", sep="" )
#---------------------------------------------------
def displayMethodStmtSetnumber( n, szStmtValue, pnStmtChild1 ):
    print( "| ", ' '*((n*2)+2), "num var name='", szStmtValue, "'", sep="" )
#---------------------------------------------------
def displayMethodStmtSetstring( n, szStmtValue, pnStmtChild1 ):
    print( "| ", ' '*((n*2)+2), "str var name='", szStmtValue, "'", sep="" )
    if (pnStmtChild1 == 0):
        szStringValue = "(don't know [error])"
    else:
        szStringValue = pnStmtChild1.getValue()
    print( "| ", ' '*((n*2)+2), "str var value='", szStringValue, "'", sep="" )
#---------------------------------------------------

#-----------------------------------------------------------------
# this stuff is all new after the expression evaluator was built. It
# is so that ilks ("our version" of classes) can be read in and stored.
# This way we can make our own objects and send them messages
#-----------------------------------------------------------------
def readIlkfile( readfileToken ):
    if (readfileToken == 0):
        expr_utilities.printError( "readIlkfile", "No file name supplied" )
        return 0
    if (readfileToken.getType() != "alphanum" ):
        expr_utilities.printError( "readIlkfile", "File name not an alphanum" )
        return 0
    readfileName = readfileToken.getValue()
    ilkfileContents = 0
    #open file, return its contents
    try:
        expr_utilities.printDebug( "Opening ilkfile " + readfileName )
        thisFileObject = open( readfileName )
        #gather the input
        ilkfileContents = thisFileObject.read()
        thisFileObject.close()
    except IOError:
        print( "ERROR: readIlkfile: IOError: Cannot open file:", readfileName )
    return( ilkfileContents )


#----------------------------
# <S>        : "ilk" ALPHANUM[ilkname] { FIELDS } METHODS
# FIELDS     : FIELD FIELDS
#            | FIELD
# FIELD      : "int" ALPHANUM[fieldname] "=" NUM ";"
#            | "str" ALPHANUM[fieldname] "=" QUOTEDSTRING ";"
# METHODS    : METHOD METHODS
#            | METHOD
# METHOD     : "method" alphanum[methodname] "{" STATEMENTS "}"
# STATEMENTS : STATEMENT STATEMENTS
#            | STATEMENT
# STATEMENT  : SHELL_STMT ";"
#            | SETNUMBER_STMT ";"
#            | SETSTRING_STMT ";"
#            | IF_STMT
#            | WHILE_STMT
#            | MAKEILKOBJ_STMT ";"
#            | SENDILKOBJ_STMT ";"
#----------------------------
# SHELL_STMT      : "shell" STRING
# ASST_STMT       : ALPHANUM[intfieldname] "=" INTEXPRESSION
#                 | ALPHANUM[strfieldname] "=" STREXPRESSION 
# MAKEILKOBJ_STMT : "makeobject" ALPHANUM[ilkname] ALPHANUM[objectname]
# SENDILKOBJ_STMT : "sendobject" ALPHANUM[ilkname] ALPHANUM[objectname] ALPHANUM[message]
# IF_STMT         : "if" "(" EXPR ")" "{" STATEMENTS "}"
#                 | "if" "(" EXPR ")" "{" STATEMENTS "}" "else" "{" STATEMENTS "}"
# WHILE_STMT      : "while" "(" EXPR ")" "{" STATEMENTS "}"
#----------------------------
# STRING          : QUOTEDSTRING
#                 | STREXPRESSION
# STREXPRESSION   : {what goes here?}
#----------------------------

#------------
# ParseIlkTokens()
#   Take an ilk file token list, return: (a) a varlist, (b) a method list
#------------
def ParseIlkTokens( ilkTokens ):
    expr_utilities.printDebug( "In ParseIlkTokens" )
    thisToken = ilkTokens
    print( "------------------111----------------" )
    while thisToken != 0:
        print( "<<<", thisToken.getType(), "+++", thisToken.getValue() )
        thisToken = thisToken.getNext()
    print( "------------------222----------------" )

    if (isParticAlphanum(ilkTokens, "ilk") == 0):
        expr_utilities.printError( "ParseIlkTokens", "1st token not 'ilk'" )
        return 0, 0
    secondToken = ilkTokens.getNext()
    if (secondToken == 0):
        expr_utilities.printError( "ParseIlkTokens", "No second token supplied" )
        return 0, 0
    if (secondToken.getType() != "alphanum" ):
        expr_utilities.printError( "ParseIlkTokens", "2nd token not an alphanum" )
        return 0, 0
    szIlkName = secondToken.getValue()
    print( "Temp: Ilk name =", szIlkName, "(placeholder)" )
    thirdToken = secondToken.getNext()
    if (isLcurly(thirdToken) == 0):
        expr_utilities.printError( "ParseIlkTokens", "3rd token not '{'" )
        return 0, 0
    expr_globals.t_CurToken = thirdToken.getNext()
    expr_globals.n_ErrorSeen = 0
    vIlkVarlist = gatherIlkVarlist()
    if (expr_globals.n_ErrorSeen != 0):
        return 0, 0
    if (expr_globals.n_Debug != 0):
        print( "----vv---ilk-vars---vv---- for ilk: ", szIlkName )
        expr_utilities.showVarList( vIlkVarlist )
        print( "----^^---ilk-vars---^^---- for ilk: ", szIlkName )

    #move past the right curly brace at the end of the vars
    if (isRcurly(expr_globals.t_CurToken) == 0):
        expr_utilities.printError( "ParseIlkTokens", "Post-var token not '}'" )
        return 0, 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

    #now gather up the methods
    mIlkMethodlist = gatherIlkMethodlist()
    if (expr_globals.n_ErrorSeen != 0):
        return 0, 0
    if (expr_globals.n_Debug != 0):
        print( "----vv---ilk-methods---vv---- for ilk:", szIlkName )
        mCurMethod = mIlkMethodlist
        while (mCurMethod != 0):
            print( "-->", mCurMethod.getName() )
            vCurArg = mCurMethod.getArgs()
            while( vCurArg != 0):
                print( "--arg-name/type/value-->", vCurArg.getName(), "/", vCurArg.getType(), "/", vCurArg.getValue() )
                vCurArg = vCurArg.getNext()
            mCurMethod = mCurMethod.getNext()
        print( "----^^---ilk-methods---^^---- for ilk:", szIlkName )

    return vIlkVarlist, mIlkMethodlist

#-----
# gather ilk var list
#-----
def gatherIlkVarlist():
    print( "Temp: gathering ilk var list (placeholder)" )
    vReturnValue = 0
    vLastVar = 0
    while( 1 ):
        if ( expr_globals.t_CurToken == 0 ):
            expr_utilities.printError( "gatherIlkVarlist", "abrupt end(1)" )
            return 0
        if isRcurly( expr_globals.t_CurToken ):
            #we reached the end of the ilk vars
            break

        #gather the next var
        if (isParticAlphanum(expr_globals.t_CurToken,"number")==0 and isParticAlphanum(expr_globals.t_CurToken,"string")==0):
            expr_utilities.printError( "gatherIlkVarlist", "no var to gather" )
            return 0
        szNewVarType = expr_globals.t_CurToken.getValue()
        if (szNewVarType == "number"):
            newVarInitValue = 0
        else:
            newVarInitValue = ""

        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        
        if (isAlphanum( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherIlkVarlist", "no name for declared var" )
            return 0
        szNewVarName = expr_globals.t_CurToken.getValue()

        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

        #see if an initial value is set by the user, if so gather it up
        if (isEqualSign( expr_globals.t_CurToken )):
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
            if ( expr_globals.t_CurToken == 0 ):
                expr_utilities.printError( "gatherIlkVarlist", "abrupt end(2)" )
                return 0
            szInitValueType = expr_globals.t_CurToken.getType()
            newVarInitValue = expr_globals.t_CurToken.getValue()
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
            #assure init value is of the right type
            if (szInitValueType != szNewVarType):
                expr_utilities.printError( "gatherIlkVarlist", "type mismatch for var: " + szNewVarName)
                return 0
            
        #make sure there's a semi-colon after the var name
        if (isSemi( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherIlkVarlist", "no ';' after var: " + szNewVarName )
            return 0
        
        #move beyond the semi-colon
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

        #make sure this var is not a repeat
        vTempVar = vReturnValue
        while( vTempVar != 0 ):
            if (vTempVar.getName() == szNewVarName):
                expr_utilities.printError( "gatherIlkVarlist", "var name seen twice: " + szNewVarName )
                return 0
            vTempVar = vTempVar.getNext()

        #ok, it's not a repeat - make a new var out of it, add to end of list

        vNewVar = expr_classes.Var( szNewVarName, szNewVarType, newVarInitValue )
        if (vLastVar == 0):
            vReturnValue = vNewVar
        else:
            vLastVar.pointTo( vNewVar )
        vLastVar = vNewVar
        
    return vReturnValue


#-----------------------------------------
# gather ilk method list
#-----------------------------------------
# METHODS    : METHOD METHODS
#            | METHOD
# METHOD     : "method" alphanum[methodname] "(" ARGS[possibly 0] ")" "{" STATEMENTS "}"
#-----------------------------------------
def gatherIlkMethodlist():
    print( "Temp: gatherIlkMethodlist()" )
    mReturnValue = 0
    mLastMethod = 0
    while( 1 ):
        if ( expr_globals.t_CurToken == 0 ):
            break
        if (isParticAlphanum( expr_globals.t_CurToken, "method" ) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "no method to gather" )
            return 0
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        if (isAlphanum( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "no name after 'method'" )
            return 0
        
        szNewMethodName = expr_globals.t_CurToken.getValue()
        print( "Temp: in loop, method name is", szNewMethodName )

        #make sure there's a lparen after the method name
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        if (isLparen(expr_globals.t_CurToken) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "No '(' after method name" )
            return 0

        #move past the lparen, gather up the method's args, move past the rparen
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        vNewMethodArgs = gatherMethodArgs()
        if (expr_globals.n_ErrorSeen != 0):
            return 0
        if (isRparen( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "No ')' after method args" )
            return 0
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

        #make sure there's a lcurly after the rparen
        if (isLcurly(expr_globals.t_CurToken) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "No '{' after method args" )
            return 0

        #move past the lcurly, gather up the method's stmts, move past the rcurly
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        expr_globals.n_ErrorSeen = 0
        pnNewMethodStatements = gatherMethodStatements()
        if (expr_globals.n_ErrorSeen != 0):
            return 0
        if (isRcurly( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherIlkMethodlist", "No '}' after method contents" )
            return 0
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

        #add this new method onto the list to return
        mNewIlkMethod = expr_classes.Method( szNewMethodName, vNewMethodArgs, pnNewMethodStatements )
        if (mLastMethod == 0):
            mReturnValue = mNewIlkMethod
        else:
            mLastMethod.pointTo( mNewIlkMethod )
        mLastMethod = mNewIlkMethod

    return mReturnValue

#-----------------------------------------
# gether up the args to a method
#   - returns a list of args, each of which which is a Var class instance
#       value is the initial val if none supplied at time method is called
#-----------------------------------------
def gatherMethodArgs():
    print( "Temp: gatherMethodArgs()" )
    vReturnValue = 0
    vLastArg = 0
    while( 1 ):
        if ( expr_globals.t_CurToken == 0 ):
            expr_utilities.printError( "gatherMethodArgs", "abrupt end(1)" )
            return 0
        if isRparen( expr_globals.t_CurToken ):
            #we reached the end of the method args
            break
        
        #gather the next arg
        if (isParticAlphanum(expr_globals.t_CurToken,"number")==0 and isParticAlphanum(expr_globals.t_CurToken,"string")==0):
            expr_utilities.printError( "gatherMethodArgs", "no arg to gather" )
            return 0
        szNewArgType = expr_globals.t_CurToken.getValue()
        if (szNewArgType == "number"):
            newArgInitValue = 0
        else:
            newArgInitValue = ""

        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        
        if (isAlphanum( expr_globals.t_CurToken ) == 0):
            expr_utilities.printError( "gatherMethodArgs", "no name for declared arg" )
            return 0
        szNewArgName = expr_globals.t_CurToken.getValue()

        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()

        #see if an initial value is set by the user, if so gather it up
        if (isEqualSign( expr_globals.t_CurToken )):
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
            if ( expr_globals.t_CurToken == 0 ):
                expr_utilities.printError( "gatherMethodArgs", "abrupt end(2)" )
                return 0
            szInitValueType = expr_globals.t_CurToken.getType()
            newArgInitValue = expr_globals.t_CurToken.getValue()
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
            #assure init value is of the right type
            if (szInitValueType != szNewArgType):
                expr_utilities.printError( "gatherMethodArgs", "type mismatch for arg: " + szNewArgName)
                return 0
            
        #make sure there's a comma after the var name
        if (isComma( expr_globals.t_CurToken )):
            #move beyond the comma
            expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        elif isRparen( expr_globals.t_CurToken == 0):
            #not a comma, but not a ')' either - this is a syntax error
            expr_utilities.printError( "gatherMethodArgs", "no ',' or ')' after arg: " + szNewArgName )
            return 0

        #make sure this arg is not a repeat
        vTempArg = vReturnValue
        while( vTempArg != 0 ):
            if vTempArg.getName() == szNewArgName:
                expr_utilities.printError( "gatherMethodArgs", "arg name seen twice: " + szNewArgName )
                return 0
            vTempArg = vTempArg.getNext()

        #ok, it's not a repeat - make a new arg out of it, add it to list

        vNewArg = expr_classes.Var( szNewArgName, szNewArgType, newArgInitValue )
        if (vLastArg == 0):
            vReturnValue = vNewArg
        else:
            vLastArg.pointTo( vNewArg )
        vLastArg = vNewArg
        
    return vReturnValue

#-----------------------------------------
# STATEMENTS : STATEMENT STATEMENTS
#            | STATEMENT
#-----------------------------------------
def gatherMethodStatements():
    print( "Temp: gatherMethodStatements()" )
    pnReturnValue = 0
    pnLastStmt = 0
    
    while( 1 ):
        expr_globals.n_ErrorSeen = 0
        pnThisStmt = gatherSingleStatement()
        if expr_globals.n_ErrorSeen != 0:
            return 0
        if (pnThisStmt == 0):
            return 0
        #add the statement to the end of the list
        if (pnLastStmt == 0):
            pnReturnValue = pnThisStmt
        else:
            pnLastStmt.pointTo( pnThisStmt )
        pnLastStmt = pnThisStmt
        if (isRcurly(expr_globals.t_CurToken)):
            break
    return( pnReturnValue )

#-----------------------------------------
# gather up a single statement including the ending semi-colon or curly brace,
#    as the case may be
#
# STATEMENT  : SHELL_STMT
#            | IF_STMT
#            | WHILE_STMT
#            | MAKEILKOBJ_STMT
#            | SENDILKOBJ_STMT
#            | ASST_STMT
#-----------------------------------------
def gatherSingleStatement():
    print( "Temp: gatherSingleStatement()" )
    expr_globals.n_ErrorSeen = 0

    #check what statement type this is and act accordingly
    tStatementType = expr_globals.t_CurToken
    if (tStatementType == 0):
        expr_utilities.printError( "gatherSingleStatement", "null stmt" )
        return 0
    #parse stmt depending on its type
    if (isParticAlphanum( tStatementType, "shell" )):        
        return( gatherSingleStmtShell() )
    if (isParticAlphanum( tStatementType, "setnumber" )):
        return( gatherSingleStmtSetNumber() )
    if (isParticAlphanum( tStatementType, "setstring" )):
        return( gatherSingleStmtSetString() )
    if (isParticAlphanum( tStatementType, "if" )):        
        return( gatherSingleStmtIf() )
    if (isParticAlphanum( tStatementType, "while" )):        
        return( gatherSingleStmtWhile() )
    if (isParticAlphanum( tStatementType, "makeilkobj" )):        
        return( gatherSingleStmtMakeilkobj() )
    if (isParticAlphanum( tStatementType, "sendilkobj" )):       
        return( gatherSingleStmtWhile() )
    
    #if we fall through to here, it's an unknown statement type
    if (isAlphanum( tStatementType )):
        expr_utilities.printError( "gatherSingleStatement", "unknown statement type: '" + tStatementType.getValue() + "'")
    else:
        expr_utilities.printError( "gatherSingleStatement", "unknown statement type (not an alphanum)" )
    return 0

#    pnReturnValue = expr_classes.Node( "expression", "" )
#    pnValueNode = expr_parser.makeMathParsetree()
#    pnReturnValue.pointToAsChild1( pnValueNode )
#    if (isSemi( expr_globals.t_CurToken )):
#        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
#    return( pnReturnValue )

#-----------------------------------------
# gatherSingleStmtShell()
#   called with global token pointer pointing to "shell" token
#   return pointer to parse tree representing shell stmt
#-----------------------------------------
def gatherSingleStmtShell():
    print( "Temp: gatherSingleStmtShell()" )
    expr_globals.n_ErrorSeen = 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (expr_globals.t_CurToken == 0):
        expr_utilities.printError( "gatherSingleStmtShell", "null shell stmt" )
        return 0
    if (expr_globals.t_CurToken.getType() != "string"):
        expr_utilities.printError( "gatherSingleStmtShell", "shell stmt non-string arg" )
        return 0
    szShellArg = expr_globals.t_CurToken.getValue()
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if isSemi( expr_globals.t_CurToken == 0 ):
        expr_utilities.printError( "gatherSingleStmtShell", "missing ';' @ end of shell stmt" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    return expr_classes.Node( "shell", szShellArg )
#-----------------------------------------
def gatherSingleStmtSetNumber():
    print( "Temp: gatherSingleStmtSetNumber()" )
    expr_globals.n_ErrorSeen = 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (expr_globals.t_CurToken == 0):
        expr_utilities.printError( "gatherSingleStmtSetNumber", "null set stmt" )
        return 0
    if (expr_globals.t_CurToken.getType() != "alphanum" ):
        expr_utilities.printError( "gatherSingleStmtSet", "no alphanum after 'setnumber'" )
        return 0
    szVarName = expr_globals.t_CurToken.getValue()
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (expr_globals.t_CurToken == 0):
        expr_utilities.printError( "gatherSingleStmtSetNumber", "no token after var name" + szVarName )
        return 0
    if (isEqualSign( expr_globals.t_CurToken )):
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        if (expr_globals.t_CurToken == 0):
            expr_utilities.printError( "gatherSingleStmtSetNumber", "no token after '='" )
            return 0
    pnValueNode = expr_parser.makeMathParsetree()
    if (isSemi( expr_globals.t_CurToken )):
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    pnReturnValue = expr_classes.Node( "setnumber", szVarName )
    pnReturnValue.pointToAsChild1( pnValueNode )
    return pnReturnValue
#-----------------------------------------
def gatherSingleStmtSetString():
    print( "Temp: gatherSingleStmtSetString()" )
    expr_globals.n_ErrorSeen = 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (expr_globals.t_CurToken == 0):
        expr_utilities.printError( "gatherSingleStmtSetString", "null set stmt" )
        return 0
    if (expr_globals.t_CurToken.getType() != "alphanum" ):
        expr_utilities.printError( "gatherSingleStmtSet", "no alphanum after 'setstring'" )
        return 0
    szVarName = expr_globals.t_CurToken.getValue()
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (expr_globals.t_CurToken == 0):
        expr_utilities.printError( "gatherSingleStmtSetString", "no token after var name" + szVarName )
    if (isEqualSign( expr_globals.t_CurToken )):
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        if (expr_globals.t_CurToken == 0):
            expr_utilities.printError( "gatherSingleStmtSetString", "no token after '='" )
            return 0
    if (expr_globals.t_CurToken.getType() != "string"):
        expr_utilities.printError( "gatherSingleStmtSetString", "non-string value for var" + szVarName )
        return 0
    varValue = expr_globals.t_CurToken.getValue()
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if isSemi( expr_globals.t_CurToken == 0 ):
        expr_utilities.printError( "gatherSingleStmtSet", "missing ';' @ end of set stmt" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    pnValueNode = expr_classes.Node( "valuetoset", varValue )
    pnReturnValue = expr_classes.Node( "setstring", szVarName )
    pnReturnValue.pointToAsChild1( pnValueNode )
    return pnReturnValue
#-----------------------------------------
def gatherSingleStmtIf():
    print( "Temp: gatherSingleStmtIf()" )
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (isLparen(expr_globals.t_CurToken) == 0):
        expr_utilities.printError( "gatherSingleStmtIf", "No '(' for condition" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    #make condition parse tree
    pnCondition = expr_parser.makeMathParsetree()
    if (isRparen(expr_globals.t_CurToken) == 0):
        expr_utilities.printError( "gatherSingleStmtIf", "No ')' after condition" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    if (isLcurly(expr_globals.t_CurToken) == 0):
        expr_utilities.printError( "gatherSingleStmtIf", "No '{' for 'if' portion" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    #gather up the statements for when condition is true
    pnStatementsIfConditionTrue = gatherMethodStatements()
    if (isRcurly(expr_globals.t_CurToken) == 0):
        expr_utilities.printError( "gatherSingleStmtIf", "No '}' after 'if' portion" )
        return 0
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    pnStatementsIfConditionFalse = 0
    if (isParticAlphanum( tStatementSendilkobj, "else" )):
        #gather up the 'else' portion
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        if (isLcurly(expr_globals.t_CurToken) == 0):
            expr_utilities.printError( "gatherSingleStmtIf", "No '{' for 'else' portion" )
            return 0
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
        #gather up the statements for when condition is false
        pnStatementsIfConditionFalse = gatherMethodStatements()
        if (isRcurly(expr_globals.t_CurToken) == 0):
            expr_utilities.printError( "gatherSingleStmtIf", "No '}' after 'else' portion" )
            return 0
        expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    pnReturnValue = expr_classes.Node( "if", 0 )
    pnReturnValue.pointToAsChild1( pnCondition )
    pnReturnValue.pointToAsChild2( pnStatementsIfConditionTrue )
    pnReturnValue.pointToAsChild3( pnStatementsIfConditionFalse )
    return pnReturnValue
#-----------------------------------------
def gatherSingleStmtWhile():
    print( "Temp: gatherSingleStmtWhile()" )
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    return 0
#-----------------------------------------
def gatherSingleStmtMakeilkobj():
    print( "Temp: gatherSingleStmtMakeilkobj()" )
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    return 0
#-----------------------------------------
def gatherSingleStmtSendilkobj():
    print( "Temp: gatherSingleStmtSendilkobj()" )
    expr_globals.t_CurToken = expr_globals.t_CurToken.getNext()
    return 0
#-----------------------------------------
