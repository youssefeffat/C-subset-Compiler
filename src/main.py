from Lexer import Lexer
#from optimizer import optimizer
from parser import Parser
from semantic import Semantic
from codeGenerator import CodeGenerator


assemblyGen = CodeGenerator()
semantic = Semantic()

# file_path = "test.c"
# with open(file_path, 'r') as file:
# 	file_content = file.read()
# stringFile = "(-(!((3+2))))"
# test1 = """
# {	
# 	int x;
# 	int y;
# 	x = 1+1;
# 	y = 1+2;
# 	debug x;
# 	debug y;
# }
# {
	
# 	int x;
# 	int y;
# 	x = 1+3;
# 	y = 1+4;
# 	debug x;
# 	debug y;
# }
# """
stringFile = """
{

int func();
int func2( int x);
int func3(int x){};
int func4(int x, int y){};

int funcCall(int x){return x};
int x;
x = funcCall(1);
debug x;

	int x;
	int y;
	x = 1+1;
	y = 1+2;
	debug x;
	debug y;
	if (x>y){
		if (x){
			debug 200;
		}else{
			debug 100;
		}
	}
	else{
		debug 000;
	}
}
	
"""

def main():
	"""
	//compilateur
	print(".start")
	for (int i=1;i<argc;i++){
		analex(argv[i]);
		while(T.type!="EOF"){
			Node N = AnaSynt();
			AnaSem(N);
			N = Optim(N);
			genCode(N);
		}
	}
	print("dbg\nhalt")
	"""
	print(".start")
	#Lexical Analysis
	lexer = Lexer(stringFile)
	tokens = lexer.work()
	#Syntax Analysis
	parser = Parser(tokens)
	it = 0 
	while parser.tokens[parser.currentPosition].value!="EOF":
		it+=1
		N = parser.AnaSynt()
		# print("N : ",N)
		semantic.AnaSem(N) 
		#N = Optimizer.Optim(N)
		print("resn",semantic.nvar)
		assemblyGen.genCode(N)
		print("drop",semantic.nvar)
	print("halt")#dbg\n
	print("it : ",it)
	


if __name__ == "__main__":
    main()

    
