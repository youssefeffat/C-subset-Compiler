from resources import Node, Data

data = Data()
operationsToAssembly = data.operationsToAssembly

class CodeGenerator:

    def __init__(self):
        self.ifLabel = 0

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
            # print("DEBUGGING NODE : ",Node)             
            return

        # # Handling assignment (nd_affect)
        # elif Node.type == "nd_affect":
        #     self.genCode(Node.children[1])  
        #     print("dup")  
        #     print("set", Node.children[0].position)  
        #     return

        # Handling assignment (nd_affect)
        elif Node.type == "nd_affect":
            if (Node.children[0].type == "nd_ref"):
                self.genCode(Node.children[1])
                print("dup")
                print("set", Node.children[0].position)
            elif (Node.children[0].type == "nd_indirection"):
                self.genCode(Node.children[0].children[0]) 
                self.genCode(Node.children[1])  
                print("write")  
            return
        
        # Handling function definition (nd_function)
        elif Node.type == "nd_function":
            print("."+ Node.value)
            print("resn", Node.nvar)
            for child in Node.children:
                self.genCode(child)
            print("push 0")
            print("ret")
            return
        
        #TODO: not sure about the Assembly syntax
        # Handling function call (nd_function_call)
        elif Node.type == "nd_function_call":
            print ("prep", Node.value)
            # print("resn", Node.nvar)
            for child in Node.children:
                if child != Node.children[0]:
                    self.genCode(child)
            print("call", len(Node.children)-1)
            return
        
        #TODO: Not sure about it !!! 
        # Handling return statement (nd_return)
        elif Node.type == "nd_return":
            self.genCode(Node.children[0])
            print("ret")
            return
        
        # Handling if statement (nd_if) with unique label jumpf l1 label, jump l2 label, .l1, .l2
        elif Node.type=="nd_if":
            #print("Node : ",Node)
            self.ifLabel += 1
            self.genCode(Node.children[0])
            print(f"jumpf l1 {self.ifLabel}")
            self.genCode(Node.children[1])
            if len(Node.children)>2:
                print("jump l2")
                print(f".l1 {self.ifLabel}")
                self.genCode(Node.children[2])
                print(f".l2 {self.ifLabel}")
            return
        
        elif Node.type=="nd_indirection":
            self.genCode(Node.children[0])
            print("read")
            return
        
        elif Node.type=="nd_address":
            print("push",Node.children[0].position)
            return

        else:
            print("NODE TYPE UNKNOWN -> no assembly transformation ",Node.type)

