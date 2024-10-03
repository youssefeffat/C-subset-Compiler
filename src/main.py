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
stringFile = """
{
	int x;
	int y;
	x = 11;
	y = 22;
	//if (0){
	//	debug x;
	//	if (0){
	//		debug 200;
	//	}else{
	//		debug 100;
	//	}
	//}
	//else{
	//	debug y;
	//}

	// test while
	//while(1){
	//	debug 300;
	//	break;
	//}
	do{
		debug 333;
	}while(1);
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
	while parser.tokens[parser.currentPosition].value!="EOF":
		N = parser.AnaSynt()
		# print("N : ",N)
		semantic.AnaSem(N) 
		#N = Optimizer.Optim(N)
		print("resn",semantic.nvar)
		assemblyGen.genCode(N)
		print("drop",semantic.nvar)
	print("halt")#dbg\n
	


if __name__ == "__main__":
    main()

    
