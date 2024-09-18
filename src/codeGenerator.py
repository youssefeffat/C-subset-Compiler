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
            print("get", Node.position)             ##TODO : Position doenst exist!!!
            return

        # Handling assignment (nd_affect)
        elif Node.type == "nd_affect":
            self.genCode(Node.children[1])  
            print("dup")  
            print("set", Node.children[0].position)  ##TODO : Position doenst exist!!!
            return
        
        # Handling if statement (nd_if) with unique label jumpf l1 label, jump l2 label, .l1, .l2
        elif Node.type=="nd_if":
            #print("Node : ",Node)
            self.ifLabel += 1
            self.genCode(Node.children[0])
            print(f"jumpf l1 {self.ifLabel}")
            self.genCode(Node.children[1])
            if len(Node.children)>2: #if no else or while statement
                print("jump l2")
                print(f".l1 {self.ifLabel}")
                self.genCode(Node.children[2])
                print(f".l2 {self.ifLabel}")
            return
        # Handling while statement (nd_loop) with unique label jumpf l1 label, jump l2 label, .l1, .l2
        elif Node.type=="nd_loop":
            self.ifLabel += 1
            print(f".l1_{self.ifLabel}")
            self.genCode(Node.children[0])
            print(f"jumpf l2_{self.ifLabel}")
            self.genCode(Node.children[1])
            print(f"jump l1_{self.ifLabel}")
            print(f".l2_{self.ifLabel}")
            return
        # Handling break statement (nd_break)
        elif Node.type=="nd_break":
            print(f"jump l2 {self.ifLabel}")
            return
        # Handling continue statement (nd_ancre)
        elif Node.type=="nd_ancre":
            print(f"jump l1 {self.ifLabel}")
            return
        else:
            print("NODE TYPE UNKNOWN -> no assembly transformation ",Node.type)

