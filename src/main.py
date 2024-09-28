from Lexer import Lexer
#from optimizer import optimizer
from parser import Parser
from semantic import Semantic
from codeGenerator import CodeGenerator
from resources import stack

#stack = stack()
assemblyGen = CodeGenerator()
semantic = Semantic()


# file_path = "test.c"
# with open(file_path, 'r') as file:
# 	file_content = file.read()
# stringFile = "(-(!((3+2))))"

# stringFile = """
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

int main(){

	int calcul0(){return 0;}

	int a;
	a = calcul0();

	int x;
	x = 1;

	int y;
	y = 2;
	y = x + y;

	int z;
	z = 3;

	debug a;
	debug x;
	debug y;
	debug z;

	return 0;
}


"""

def main():
	"""
	"""
	semantic.begin()
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
		semantic.AnaSem(N) 
		#N = Optimizer.Optim(N)
		assemblyGen.genCode(N)
		print ("N : ",N)
	semantic.end()
	# print("halt")#dbg\n
	


if __name__ == "__main__":
    main()

    
