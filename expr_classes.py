import expr_scanner
import expr_execute
import expr_globals

#-----------------------------------------
class Token:
    def __init__(self, tokenType, tokenValue):
        self.myType = tokenType
        self.myValue = tokenValue
        self.next = 0
        self.prev = 0
        
    def getType(self):
        return self.myType

    def getValue(self):
        return self.myValue

    def getNext(self):
        return self.next

    def getPrev(self):
        return self.prev

    def pointTo(self, nextToken):
        self.next = nextToken

    def pointBackTo(self, prevToken):
        self.prev = prevToken

#-----------------------------------------
class Node:
    def __init__(self, nodeType, nodeValue):
        self.myType = nodeType
        self.myValue = nodeValue
        self.child1 = 0
        self.child2 = 0
        self.child3 = 0
        self.next = 0
        
    def getType(self):
        return self.myType
            
    def getValue(self):
        return self.myValue

    def getChild1(self):
        return self.child1

    def getChild2(self):
        return self.child2
    
    def getChild3(self):
        return self.child3

    def getNext(self):
        return self.next
    
    def pointToAsChild1(self, someNode):
        self.child1 = someNode
    
    def pointToAsChild2(self, someNode):
        self.child2 = someNode
    
    def pointToAsChild3(self, someNode):
        self.child3 = someNode
    
    def pointTo(self, nextNode):
        self.next = nextNode
        
#-----------------------------------------
class Var:
    def __init__(self, varName, varType, varValue):
        self.myName = varName
        self.myType = varType
        self.myValue = varValue
        self.next = 0
        
    def getName(self):
        return self.myName

    def getType(self):
        return self.myType

    def getValue(self):
        return self.myValue

    def getNext(self):
        return self.next

    def setValue(self, varValue):
        self.myValue = varValue

    def pointTo(self, nextVar):
        self.next = nextVar

#-----------------------------------------
class Readfile:
    def __init__(self, readfileName ):
        self.myName = readfileName
        self.myLines = 0
        self.curLineNo = 0
        self.numberOfLines = 0
        self.next = 0
        
    def getName(self):
        return self.myName

    def getNext(self):
        return self.next

    def pointTo(self, nextReadfile):
        self.next = nextReadfile

    def gatherInput(self, pythonFileObject):
        self.myLines = pythonFileObject.readlines()
        self.numberOfLines = len( self.myLines )
        self.curLineNo = 0

    def getLine(self):
        #return a line, or 0 if we're at end-of-file
        if (self.curLineNo >= self.numberOfLines):
            return 0
        self.curLineNo = self.curLineNo + 1
        return self.myLines[self.curLineNo - 1]

#-----------------------------------------
class Ilk:
    def __init__(self, ilkTokenlist, ilkVarlist, ilkMethodlist):
        self.myName = ilkTokenlist.getNext().getValue()
        self.myTokenlist = ilkTokenlist
        self.myVarlist = ilkVarlist
        self.myMethodlist = ilkMethodlist
        self.next = 0
        
    def getName(self):
        return self.myName

    def getVarlist(self):
        return self.myVarlist

    def getMethodlist(self):
        return self.myMethodlist

    def getNext(self):
        return self.next
    
    def pointTo(self, nextIlk):
        self.next = nextIlk

#-----------------------------------------
class Method:
    def __init__(self, methodName, methodArgs, methodTree):
        self.myName = methodName
        self.myArgs = methodArgs
        self.myTree = methodTree
        self.next = 0
        
    def getName(self):
        return self.myName

    def getArgs(self):
        return self.myArgs

    def getTree(self):
        return self.myTree

    def getNext(self):
        return self.next
    
    def pointTo(self, nextMethod):
        self.next = nextMethod
        
#-----------------------------------------
class Object:
    def __init__(self, objectIlk, objectName, objectVarlist):
        self.myIlk = objectIlk
        self.myName = objectName
        self.myVarlist = objectVarlist
        self.next = 0
        
    def getIlk(self):
        return self.myIlk

    def getName(self):
        return self.myName
        
    def getVarlist(self):
        return self.myVarlist
    
    def getNext(self):
        return self.next

    def pointTo(self, nextObject):
        self.next = nextObject
        
