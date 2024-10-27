class Optimizer:
    def __init__(self):
        self.Node = None
    
    def optim(self, Node):
        self.Node = Node
        for child in self.Node.children:
            self.optim(child)
        
        #SWITCH CASE
        
        ## 1st Layer Constant folding 
        ## ADDITION / SOUSTRACTION / MULTIPLICATION / DIVISION / MOINS_UNAIRE
        if self.Node.type == "nd_add":
            if self.Node.children[0].type == "nd_const" and self.Node.children[1] == "nd_const":
                return Node("nd_const", self.Node.children[0].value + self.Node.children[1].value)
            else:
                return Node
        elif self.Node.type == "nd_sub":
            if self.Node.children[0].type == "nd_const" and self.Node.children[1] == "nd_const":
                return Node("nd_const", self.Node.children[0].value - self.Node.children[1].value)
            
        elif self.Node.type == "nd_mul":
            if self.Node.children[0].type == "nd_const" and self.Node.children[1] == "nd_const":
                return Node("nd_const", self.Node.children[0].value * self.Node.children[1].value)

        elif self.Node.type == "nd_div":
            if self.Node.children[0].type == "nd_const" and self.Node.children[1] == "nd_const":
                return Node("nd_const", self.Node.children[0].value / self.Node.children[1].value)

        elif self.Node.type == "MOINS_UNAIRE":
            if self.Node.children[0].type == "nd_const":
                return Node("nd_const", -self.Node.children[0].value)
        else:
            return Node
        