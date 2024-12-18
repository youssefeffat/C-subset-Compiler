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

        elif self.checkType(['IDENTIFIER']):
            A = Node("nd_ref",self.tokens[self.currentPosition-1].value)
            return A        
        
        # elif self.tokens[self.currentPosition].type == "EOF":
        #     return None
        
        else:
            raise SyntaxError(f"Atomic token expected. I got {self.tokens[self.currentPosition]}, ")

    def s(self)->Node:
        """
        S := A ( '(' ( epsilon|E (','E)* ) ')' )?
          := A ( '[' E ']' )?
        
        """
        R = self.a()
        if self.checkValue(["("]):
            C = R
            R = Node("nd_function_call", self.tokens[self.currentPosition-2].value)                          
            R.addChild(C)
            if (self.checkValue([")"])):
             pass
            else :
                R.addChild(self.e(0))
                while (not self.checkValue([")"])):
                    self.acceptValue([","])
                    R.addChild(self.e(0))   
        elif self.checkValue(["["]):
            A = R
            R = Node("nd_indirection", None)
            Add = Node("nd_PLUS", None)
            Add.addChild(A)
            Add.addChild(self.e(0))
            R.addChild(Add)
            self.acceptValue(["]"])   
        return R



    def p(self)->Node:
        """
        operateur unaire
        P:= +P | -P | !P | &P | *P | S
        
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
        elif self.checkValue(["&"]):
            A = Node("nd_address",self.tokens[self.currentPosition-1].value)
            A.addChild(self.p())
            return A
        elif self.checkValue(["*"]):
            A = Node("nd_indirection",self.tokens[self.currentPosition-1].value)
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
            priority = None if signDict is None else signDict.get("priority")
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
    

    ## DONE : 'int' 'IDENTIFIER' '=' 'E' ';' is not handeled
    # *not requested 
    def i(self)->Node:
        """
        """
        # # the case of an :'debug' E ';
        if (self.tokens[self.currentPosition].value == 'debug'):	
            I =  Node("nd_debug",self.tokens[self.currentPosition].value)
            self.currentPosition += 1
            E = self.e(0)
            I.addChild(E)
            self.acceptValue([";"])


        elif (self.checkValue(["break"])):    
            I = Node("nd_break", None)
            self.acceptValue([";"])
        elif (self.checkValue(["continue"])):    
            I = Node("nd_continue", None)
            self.acceptValue([";"])
        #type: ignore # the case of an : '{'  I* '}'
        elif (self.checkValue(['{'])):     
            I = Node("nd_block", None)                          
            while(not self.checkValue(['}'])):
                I.addChild(self.i())

        # the case of an : 'int' '*'* IDENTIFIER ';'
        elif self.checkValue(["int"]):
            while (self.checkValue(["*"])):
                pass
            self.acceptType(["IDENTIFIER"])
            if self.checkValue(["("]):
                self.currentPosition -= 3
                I = self.f()
            else:
                I = Node("nd_decl",self.tokens[self.currentPosition-1].value)
                self.acceptValue([";"])
            return I
        # the case of an : if '(' E ')' I (else I)?
        elif self.checkValue(["if"]):
            I = Node("nd_if", None)
            self.acceptValue(["("])
            I.addChild(self.e(0))
            self.acceptValue([")"])
            I.addChild(self.i())
            if (self.checkValue(["else"])):
                I.addChild(self.i())
            return I
        
        # the case of an : while '(' E ')' I
        elif self.checkValue(["while"]):
            C = Node("nd_if", None)
            self.acceptValue(["("])
            E = self.e(0)
            self.acceptValue([")"])
            I = self.i()
            C.addChild(E)
            C.addChild(I)
            C.addChild(Node("nd_break", None))
            L = Node("nd_loop", "while")
            L.addChild(Node("nd_ancre", None))
            L.addChild(C)
            return L
        
        elif self.checkValue(["do"]):
            C = Node("nd_if", None)
            I = self.i()
            self.acceptValue(["while"])
            self.acceptValue(["("])
            E = self.e(0)
            self.acceptValue([")"])
            self.acceptValue([";"])
            N = Node("NOT", None)
            N.addChild(E)
            C.addChild(N)
            # C.addChild(I)
            C.addChild(Node("nd_break", None))
            L = Node("nd_loop", "do")
            L.addChild(Node("nd_ancre", None))
            L.addChild(I)
            L.addChild(C)
            return L        
        # the case of an : for '(' E ';' E ';' E ')' I
        elif self.checkValue(["for"]):
            S = Node("nd_seq", None)
            self.acceptValue(["("])
            E1 = self.e(0)
            S.addChild(E1)
            self.acceptValue([";"])
            E2 = self.e(0)
            self.acceptValue([";"])
            E3 = self.e(0)
            self.acceptValue([")"])
            L = Node("nd_loop", "for")
            C = Node("nd_if", None)
            C.addChild(E2)
            I = self.i()
            C.addChild(I)
            C.addChild(Node("nd_break", None))
            L.addChild(C)
            L.addChild(Node("nd_ancre", None))
            L.addChild(E3)
            S.addChild(L)
            return S
        elif self.checkValue(["return"]):
            I = Node("nd_return", None)                          
            I.addChild(self.e(0))
            self.acceptValue([";"])
            return I
        # the case of an : E ';'
        else:
            I = Node("nd_drop", None)                           
            I.addChild(self.e(0))
            self.acceptValue([";"])
        return I

    def f(self)->Node : 
        """
        F: "int" "IDENTIFIER" "(" "int" "IDENTIFIER" ("," "int" "IDENTIFIER" )* ")" 
        - if 'int' 'Identfier' then not '(' then pos-2 and call i
        HYPOTHESE :
        - le code doit commencer par 'int'
        ISSUES :
        - les arguments de la fonction sont de type 'int' et int et declarer
        - cannot use an argument variable directly in the function
        ANALYSE Semntique:
        - on verifie que les arguments appeler dans la fonction sont parmis les argumrnts 
        - les argument doivent etre declarer dans le scope de la function
        """
        if self.checkValue(["int"]):
            self.acceptType(["IDENTIFIER"])
            if self.checkValue(["("]):
                I = Node("nd_function", self.tokens[self.currentPosition-2].value)
                # case where 'int' 'IDENT' '(' ')'
                if self.checkValue([")"]):    
                    I.addChild(self.i())
                # case with multiple arguments
                else:
                    self.acceptValue(["int"])
                    self.acceptType(["IDENTIFIER"])
                    Narguments = Node("nd_decl", self.tokens[self.currentPosition-1].value)
                    I.addChild(Narguments)
                    while (not self.checkValue([")"])):
                        self.acceptValue([","])
                        self.acceptValue(["int"])
                        self.acceptType(["IDENTIFIER"])
                        Narguments = Node("nd_decl", self.tokens[self.currentPosition-1].value)
                        I.addChild(Narguments)
                    I.addChild(self.i())
                return I
            else :
                self.currentPosition -= 2
                I = self.i()
            return I
        raise SyntaxError(f"Expected 'int' but found {self.tokens[self.currentPosition].value}")

        
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
            raise SyntaxError(f"Expected {value} but found {self.tokens[self.currentPosition].value} at line {self.tokens[self.currentPosition].line}")        
        else:
            self.currentPosition += 1
            return True



