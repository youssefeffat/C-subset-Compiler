class Node:
    def __init__(self, type:str, value:str):
        self.type = type
        self.value = value
        self.children = []
        self.position = None
        self.nvar = None

    def addChild(self, child:'Node')->None:
        self.children.append(child)

    def __repr__(self) -> str:
        return f"Node(type={self.type}, value={self.value}, children={self.children})"
    
class Token:
    def __init__(self, type, line, value):
        self.type = type
        self.line = line
        self.value = value

    def __repr__(self) -> str:
        return f"Token(type='{self.type}', line={self.line}, value='{self.value}')"

class Symb: 
    """
    Represents a symbol (variable) in the symbol table.
    """
    def __init__(self, name: str, type: str):
        self.name = name  # Variable name
        self.type = type  # Variable type
        self.position = None  

    def __str__(self):
        return f"{self.name} ({self.type})"

    def __repr__(self):
        return str(self)
    

class Data: 
    def __init__(self):
        self.operationsPriority = {
        '*': {'priority': 7, 'nd_name': "nd_MUL", 'associativity': 1},
        '/': {'priority': 7, 'nd_name': "nd_DIV", 'associativity': 1},
        '%': {'priority': 7, 'nd_name': "nd_MOD", 'associativity': 1},
        '+': {'priority': 6, 'nd_name': "nd_PLUS", 'associativity': 1},
        '-': {'priority': 6, 'nd_name': "nd_MINUS", 'associativity': 1},
        '>=': {'priority': 5, 'nd_name': "nd_GTE", 'associativity': 1},
        '<=': {'priority': 5, 'nd_name': "nd_LTE", 'associativity': 1},
        '>': {'priority': 5, 'nd_name': "nd_GT", 'associativity': 1},
        '<': {'priority': 5, 'nd_name': "nd_LT", 'associativity': 1},
        '==': {'priority': 4, 'nd_name': "nd_EQ", 'associativity': 1},
        '!=': {'priority': 4, 'nd_name': "nd_NEQ", 'associativity': 1},
        '&&': {'priority': 3, 'nd_name': "nd_AND", 'associativity': 1},
        '||': {'priority': 2, 'nd_name': "nd_OR", 'associativity': 1},
        '=': {'priority': 1, 'nd_name': "nd_affect", 'associativity': 0}
        }
        
        self.valueToNodeType={
        "+": "nd_PLUS",
        "-": "nd_MINUS",
        "/": "nd_DIV",
        "%": "nd_MOD",
        "==": "nd_EQ",
        "!=": "nd_NEQ",
        ">=": "nd_GTE",
        "<=": "nd_LTE",
        ">": "nd_GT",
        "<": "nd_LT",
        "&&": "nd_AND",
        "||": "nd_OR",
        "=": "nd_affect",
        "*": "nd_MUL",
        }
        self.operationsToAssembly = {
            # 'Node Type' : 'Assembly code' 
            "nd_PLUS":"add",
            "nd_MINUS":"sub",
            "nd_DIV": "div",
            "nd_MOD": "mod",
            "nd_MUL" : "mul",
            "nd_debug": "dbg",

        }
        self.symbolsToNodeType = {
            "(": "nd_OPEN_PARENTHESIS",
            ")": "nd_CLOSE_PARENTHESIS",
            "{": "nd_OPEN_BRACE",
            "}": "nd_CLOSE_BRACE",
            ";": "nd_SEMICOLON",
            ",": "nd_COMMA",
            
        }



