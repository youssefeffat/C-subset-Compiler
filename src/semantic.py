from resources import Node, Symb

class Semantic:
    """
   
    """
    def __init__(self, ):
        self.nvar = 0  # Variable counter
        self.stack = []  # Symbol table stack
         # Start the first scope

    def AnaSem(self,N:Node)->Node:
        """

        """
        
        # Switch case based on the node type
        if N.type == "nd_affect":
            if N.children[0].type != "nd_ref" and N.children[0].type != "nd_indirection":
                raise ReferenceError("Expected reference node on the left-hand side of assignment.")
            for child in N.children:
                self.AnaSem(child)
            ##print ("stack : ", self.stack)
            return

        elif N.type == "nd_decl":
            S = self.declare(N.value, "int")
            S.type = "int"  
            S.position = self.nvar
            self.nvar += 1
            ##print ("stack : ", self.stack)
            return

        #TODO : potential issue with the position of the variable / Node
        elif N.type == "nd_ref":
            # print ("nd_ref")
            # Find the symbol in the current scope
            S = self.find(N.value)
            if S.type != "int":
                raise KeyError(f"Invalid reference type for {N.value}, expected integer.")
            N.position = S.position
            # print ("call of anaSem | Case : nd_ref")
            # print ("N : ", N)
            # print ("S : ", S)
            # print ("stack : ", self.stack)
            return


        elif N.type == "nd_block":
            # Start a new scope
            self.begin()
            # Recursively process each child node in the block
            for child in N.children:
                self.AnaSem(child)
            # End the current scope
            self.end()
            ##print ("stack : ", self.stack)
            return
        
        #TODO : should we check if the function have a return statement
        elif N.type == "nd_function":
            S = self.declare(N.value, "function")
            S.type = "function"  
            # Start a new scope
            self.begin() 
            self.nvar = 0
            # Recursively process each child node in the block
            for child in N.children:
                self.AnaSem(child)
            # End the current scope
            NumChildren = len(N.children)
            N.nvar = self.nvar - (NumChildren-1)
            self.end()
            return   
       
        elif N.type == "nd_function_call":
            if N.children[0].type != "nd_ref":
                raise ReferenceError("Expected reference node on the left-hand side of assignment.")
            else : 
                S = self.find(N.children[0].value)
                if S.type != "function":
                    raise KeyError(f"Invalid reference type for {N.value}, expected function.")
                for child in N.children:
                    if child != N.children[0]:
                        self.AnaSem(child)
            ##print ("stack : ", self.stack)
            # N.nvar = self.nvar - (len(N.children)-1)                #TODO : check if it's correct
            # print ("stack : ", self.stack)
            return
        
        #TODO : is it nd_ref or nd_decl
        elif N.type == "nd_address":
            if N.children[0].type != "nd_ref": 
                raise ReferenceError(" Expected reference node on the left-hand side of assignment.")
            else : 
                for child in N.children:
                    self.AnaSem(child)
            ##print ("stack : ", self.stack)
            return


        else:
            # Default case: recursively process children
            for child in N.children:
                self.AnaSem(child)
            ##print ("stack : ", self.stack)
            return
        
        
    

    def begin(self) -> None:
        """
        Begin a new scope by pushing an empty dictionary to the stack.
        This dictionary will contain the symbols (variables) for the current scope.
        """
        self.stack.append({})  # Push a new empty dictionary (scope) to the stack

    def end(self) -> None:
        """
        End the current scope by popping the top dictionary from the stack.
        """
        if self.stack:
            self.stack.pop()  # Remove the current scope (dictionary) from the stack
        else:
            raise KeyError("No scope to pop from the stack")

    def declare(self, var: str, type: str) -> Symb:
        """
        Declare a new variable in the current scope (top of the stack).
        If the variable already exists in the current scope, raise an exception.
        """
        if not self.stack:
            raise KeyError("No scope to declare variable in")

        current_scope = self.stack[-1]  # Get the top of the stack (current scope)

        if var in current_scope:
            raise KeyError(f"Variable '{var}' already declared in the current scope")
        
        # Create a new symbol (Symb) and add it to the current scope
        symbol = Symb(var, type)
        current_scope[var] = symbol
        return symbol

    def find(self, var: str) -> Symb:
        """
        Search for a variable in the stack of dictionaries (scopes).
        Start from the top (current scope) and search downwards.
        """
        for scope in reversed(self.stack):
            if var in scope:
                return scope[var]  # Return the found symbol
        raise KeyError(f"Variable '{var}' was not declared")
    
