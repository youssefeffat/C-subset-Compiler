from resources import Node, Data

data = Data()
operationsToAssembly = data.operationsToAssembly

class CodeGenerator:

    def __init__(self):
        pass

    def genCode(self,Node:Node)->None:
        """
        """
        if Node is None:
            raise Exception("WARNING Node is None")
            return
        
        if (Node.type in operationsToAssembly):
            for child in Node.children:
                self.genCode(child)
            print(operationsToAssembly[Node.type])
        
        elif Node.type=="NUMERIC_LITERAL": 
            print("push",Node.value)
        
        elif Node.type=="NOT":
            self.genCode(Node.children[0])
            print("not")
        
        elif Node.type=="MOINS_UNAIRE":
            print("push 0")
            self.genCode(Node.children[0])
            print("sub")
        
        # 
        elif Node.type=="nd_block":
            for child in Node.children:
                self.genCode(child)
            # self.genCode(Node.children[0])
        
        elif Node.type=="nd_drop":
            self.genCode(Node.children[0])
            print("drop 1")

        # Handling variable declaration (nd_decl)
        elif Node.type == "nd_decl":
            return

        # Handling variable reference (nd_ref)
        elif Node.type == "nd_ref":
            print("get", Node.position)             
            return

        # Handling assignment (nd_affect)
        elif Node.type == "nd_affect":
            self.genCode(Node.children[1])  
            print("dup")  
            print("set", Node.children[0].position)  ##TODO : Position doenst exist!!!
            return
        
        # Handling function definition (nd_function)
        elif Node.type == "nd_function":
            print(".", Node.value)
            print("resn", Node.nvar)
            self.genCode(Node.children[0])
            print("push 0")
            print("ret")
            return
        
        else:
            print("NODE TYPE UNKNOWN -> no assembly transformation ",Node.type)

