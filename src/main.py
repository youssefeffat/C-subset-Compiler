from Lexer import Lexer
# from optimizer import optimizer
from parser import Parser
from semantic import Semantic
from codeGenerator import CodeGenerator
from resources import stack

assemblyGen = CodeGenerator()
semantic = Semantic()

file_path = './CFilesTests/test.c'
with open(file_path, 'r') as file:
	file_content = file.read()

def main():
	"""
	"""
	semantic.begin()

	print(".start")
	print("prep main")
	print("call 0")
	print("halt")
	#Lexical Analysis
	lexer = Lexer(file_content)
	tokens = lexer.work()
	#Syntax Analysis
	parser = Parser(tokens)
	# it = 0 
	while parser.tokens[parser.currentPosition].value!="EOF":
		# it+=1
		N = parser.AnaSynt()
		semantic.AnaSem(N) 
		#N = Optimizer.Optim(N)
		print("resn", semantic.nvar)
		assemblyGen.genCode(N)
		print("drop", semantic.nvar)	

	semantic.end()
	# print("halt")#dbg\n
	


if __name__ == "__main__":
    main()

    
# file_content = """
# int calcul0(){return 1;}
# int calculx(int x){return x;}
# int calculxplus1(int x){ int x; x=x+1; return x;}
# int calculXAddY(int x, int y){int res; res=x+y; return res;}
# int GRondF(int x){ int f; f = calculx(x)+1; return f;} 

# int main(){
# 	int *a;
# 	a = calcul0();

# 	int x;
#  	x = calculx(a);

# 	int x1;
# 	x1 = calculxplus1(x);

# 	int y;
# 	y = 1;
# 	//y = calculXAddY(x1,y);

# 	int f;
# 	f = GRondF(calculx(y));

# 	debug a;
#     debug x;
# 	debug x1;
# 	debug y;
# 	debug f;

# 	return 0;
# }
# """