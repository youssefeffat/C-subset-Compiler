from resources import Data, Token, Node

Data = Data()
OperationsToAssembly = Data.operationsToAssembly
operationsPriority = Data.operationsPriority
valueToNodeType = Data.valueToNodeType
symbolsToNodeType = Data.symbolsToNodeType

class Parser:
    """
    regarde le contexte local
    """
    def __init__(self,tokens: list[Token]):
        self.tokens = tokens
        self.currentPosition = 0

    def AnaSynt(self)->Node:
        """
        appelle la bonne fonction pour le token courant
        gros switch
        """
        return self.f()
    
    def a(self)->Node|None:
        """
        A:= cste | '('E')' | 'Id' '=' 'E'
        """
        if self.checkType(["NUMERIC_LITERAL"]): 
            A = Node("NUMERIC_LITERAL",self.tokens[self.currentPosition-1].value)
            return A
        elif self.checkValue(["("]):
            A = self.e(0)
            self.acceptValue([")"])
            return A

        ##TODO : fix the issue when "debug x;" the node representing x is not of type nd_decl 
        elif self.checkType(['IDENTIFIER']):
            A = Node("nd_ref",self.tokens[self.currentPosition-1].value)
            return A        
        
        # elif self.tokens[self.currentPosition].type == "EOF":
        #     return None
        
        else:
            raise SyntaxError(f"Atomic token expected. I got {self.tokens[self.currentPosition]}")

    def s(self)->Node:
        """
        S := A ( '(' ( epsilon|E (','E)* ) ')' )?
        
        """
        A = self.a()
        if self.checkValue(["("]):
            S = Node("nd_function_call", None)                          #TODO Node Value is None ????? 
            S.addChild(A)
            if (not self.checkValue([")"])):
                S.addChild(self.e(0))
                while (not self.checkValue([")"])):
                    self.acceptValue([","])
                    S.addChild(self.e(0))
            return S
        else:
            return self.a()


    def p(self)->Node:
        """
        operateur unaire
        P:= +P | -P | !P | S
        """
        if self.checkValue(["+"]):
            A = Node("PLUS_UNAIRE",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        elif self.checkValue(["-"]):
            A = Node("MOINS_UNAIRE",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        elif self.checkValue(["!"]):
            A = Node("NOT",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        else:
            return self.s()

    def m(self)->Node:
        """e pour epsilon
        M:= E'*'M | M := M(e|'+'E)
        """
        return self.p()

    def e(self,prio:int)->Node:
        """e pour epsilon
        operateur binaire
        une expression represente une valeur
        E:= M(e|'+'E|'-'E)
        E:=E'*'E|E'/'E|...|P
        """
        A1 = self.p()
        while (self.tokens[self.currentPosition].type!="EOF" ):
            signDict = operationsPriority.get(self.tokens[self.currentPosition].value) # type: ignore # priority dict of the current token
            priority = None if signDict is None else signDict.get("priority") #TODO:DONE Change with Data.operationsPriority 
            associativity = None if signDict is None else signDict.get("associativity")
            nd_type = valueToNodeType.get(self.tokens[self.currentPosition].value)
            tk_value = self.tokens[self.currentPosition].value
            if (priority is None or priority<prio):
                return A1
            
            self.currentPosition += 1
            A2 = self.e(priority + associativity)
            if (nd_type is None):
                raise TypeError("nd_type is none, value: ",self.tokens[self.currentPosition].value)
            A0 = Node(nd_type,tk_value)
            A0.addChild(A1)
            A0.addChild(A2)
            A1 = A0
        return A1
    

    ## TODO there is an issue with choosing  between the types of the token and the node
    ## TODO : 'int' 'IDENTIFIER' '=' 'E' ';' is not handeled
    def i(self)->Node:

        # # the case of an :'debug' E ';
        if (self.tokens[self.currentPosition].value == 'debug'):	
            I =  Node("nd_debug",self.tokens[self.currentPosition].value)
            self.currentPosition += 1
            E = self.e(0)
            I.addChild(E)
            self.acceptValue([";"])

        #type: ignore # the case of an : '{'  I* '}'
        elif (self.checkValue(['{'])):      
            I = Node("nd_block", None)                          #TODO Node Value is None ?????
            while(not self.checkValue(['}'])):
                I.addChild(self.i())

        # the case of an : 'int' IDENTIFIER ';'
        elif self.checkValue(["int"]):
            self.acceptType(["IDENTIFIER"])
            I = Node("nd_decl",self.tokens[self.currentPosition-1].value)
            self.acceptValue([";"])
            return I
        
        # the case of an : E ';'
        else:
            I = Node("nd_drop", None)                           #TODO Node Value is None ?????
            I.addChild(self.e(0))
            self.acceptValue([";"])
        return I

    def f(self)->Node : 
        """
        F: "int" IDENTIFIER "(" "int" IDENTIFIER ("," "int" IDENTIFIER )* ")" ";"
        
        """
        if self.checkValue(["int"]):
            self.checkType(["IDENTIFIER"])
            I = Node("nd_decl",self.tokens[self.currentPosition-1].value)
            if self.checkValue(["("]):
                # case where 'int' 'IDENT' '(' ')'';'
                if self.checkValue([")"]):
                    I.addChild(Node("nd_function", None))
                    self.checkValue([';'])
                # case with multiple arguments
                else:
                    while (not self.checkValue([")"])):
                        self.acceptType(["IDENTIFIER"])
                        self.acceptValue([","])
                    I.addChild(self.i())
            else :
                self.acceptValue([';'])
            return I
        return self.i()

    def checkType(self,type: list[str])->bool:
        if (self.tokens[self.currentPosition].type not in type):
            return False
        else:
            self.currentPosition += 1
            return True

    def acceptType(self, type: list[str]) -> bool:
        if self.tokens[self.currentPosition].type not in type:
            raise SyntaxError(f"Unexpected token type: {self.tokens[self.currentPosition].type}\nline {self.tokens[self.currentPosition].line}, token expected: {type}")
        else:
            self.currentPosition += 1
            return True
        
    def checkValue(self,value: list[str])->bool:
        if (self.tokens[self.currentPosition].value not in value):
            return False
        else:
            self.currentPosition += 1
            return True
        
    ## TODO : add the line number to the error message
    def acceptValue(self, value:list[str]) -> bool:
        if self.tokens[self.currentPosition].value not in value:
            raise SyntaxError(f"Expected {value} but found {self.tokens[self.currentPosition].value}")        
        else:
            self.currentPosition += 1
            return True


