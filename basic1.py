###################################################################
# IMPORTS                                                         #
###################################################################

from strings_with_arrows import *

####################################################################
# CONSTANTS                                                        #
####################################################################

DIGITS = '0123456789'

#####################################################################
# ERROER : Verschiedene Arten von Fehlern, die während der          #
# Ausführung auftreten können                                       #
#####################################################################

class Error:
	def __init__(self, pos_start, pos_end, error_name, details):
		self.pos_start = pos_start
		self.pos_end = pos_end
		self.error_name = error_name
		self.details = details
	
	def as_string(self):
		result  = f'{self.error_name}: {self.details}\n'
		result += f'File {self.pos_start.fn}, line {self.pos_start.line_number}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

class IllegalCharError(Error):
	def __init__(self, pos_start, pos_end, details):
		super().__init__(pos_start, pos_end, 'Illegal Character', details)

class InvalidSyntaxError(Error):
	def __init__(self, pos_start, pos_end, details=''):
		super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
	def __init__(self, pos_start, pos_end, details, context):
		super().__init__(pos_start, pos_end, 'Runtime Error', details)
		self.context = context

	def as_string(self):
		result  = self.generate_traceback()
		result += f'{self.error_name}: {self.details}'
		result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
		return result

	def generate_traceback(self):
		result = ''
		pos = self.pos_start
		ctx = self.context

		while ctx:
			result = f'  File {pos.fn}, line {str(pos.line_number)}, in {ctx.display_name}\n' + result
			pos = ctx.parent_entry_pos
			ctx = ctx.parent

		return 'Traceback (most recent call last):\n' + result

#######################################################################
# POSITION : Dies wird verwendet, um die Position des Tokens im       #
# Falle eines Fehlers nachzuverfolgen                                 #
#######################################################################

class Position:
	def __init__(self, idx, ln, col, fn, ftxt, line_number):
		self.idx = idx
		self.ln = ln
		self.col = col
		self.fn = fn
		self.ftxt = ftxt
		self.line_number = line_number

	def advance(self, current_char=None):
		self.idx += 1
		self.col += 1

		if current_char == '\n':
			self.ln += 1
			self.col = 0

		return self

	def copy(self):
		return Position(self.idx, self.ln, self.col, self.fn, self.ftxt, self.line_number)

#######################################################################
#  TOKEN : Ein Token ist eine Eingabe, die einen Typ und einen Wert   #
# hat, z. B. ein Operator wie +, -, *, /, ^ oder eine Klammer ()      #
#######################################################################

TT_INT			= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MUL      = 'MUL'
TT_DIV      = 'DIV'
TT_POW			= 'POW'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF			= 'EOF'

class Token:
	def __init__(self, type_, value=None, pos_start=None, pos_end=None):
		self.type = type_
		self.value = value

		if pos_start:
			self.pos_start = pos_start.copy()
			self.pos_end = pos_start.copy()
			self.pos_end.advance()

		if pos_end:
			self.pos_end = pos_end
	
	def __repr__(self):
		if self.value: return f'{self.type}:{self.value}'
		return f'{self.type}'

#########################################################################
# LEXER                                                                 #
# Die klasse 'Lexer' scannt die eingabezeichen,prüft auf lexikalishe    #
# Korrektheit und weist jedem Zeichen enen Tokentyp                     #
#########################################################################

class Lexer:
	def __init__(self, fn, text, line_number):
		self.fn = fn
		self.text = text
		self.pos = Position(-1, 0, -1, fn, text, line_number)
		self.current_char = None
		self.advance()
	
	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

	def make_tokens(self):
		tokens = []

		while self.current_char != None:
			if self.current_char in ' \t':
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char == '+':
				tokens.append(Token(TT_PLUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '-':
				tokens.append(Token(TT_MINUS, pos_start=self.pos))
				self.advance()
			elif self.current_char == '*':
				tokens.append(Token(TT_MUL, pos_start=self.pos))
				self.advance()
			elif self.current_char == '/':
				tokens.append(Token(TT_DIV, pos_start=self.pos))
				self.advance()
			elif self.current_char == '^':
				tokens.append(Token(TT_POW, pos_start=self.pos))
				self.advance()
			elif self.current_char == '(':
				tokens.append(Token(TT_LPAREN, pos_start=self.pos))
				self.advance()
			elif self.current_char == ')':
				tokens.append(Token(TT_RPAREN, pos_start=self.pos))
				self.advance()
			else:
				pos_start = self.pos.copy()
				char = self.current_char
				self.advance()
				return [], IllegalCharError(pos_start, self.pos, "'" + char + "'") # Eine leere Liste [] für Tokens (keine Tokens bei Fehlern)

		tokens.append(Token(TT_EOF, pos_start=self.pos))
		return tokens, None #Dieses None ist für die Fehler; falls Fehler auftreten, wird diese Zeile nicht ausgeführt.

	def make_number(self):  
		num_str = ''
		dot_count = 0
		pos_start = self.pos.copy()  # 245.536 * 20,   245.53.2

		while self.current_char != None and self.current_char in DIGITS + '.':
			if self.current_char == '.':
				if dot_count == 1: break
				dot_count += 1
				num_str += '.'
			else:
				num_str += self.current_char
			self.advance()

		if dot_count == 0:
			return Token(TT_INT, int(num_str), pos_start, self.pos)
		else:
			return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

########################################################################
# NODES : Verschiedene Arten von Knoten, die beim Aufbau des           #
# abstrakten Syntaxbaums (Abstract Syntax Tree) helfen                 #
########################################################################

class NumberNode:
	def __init__(self, tok):
		self.tok = tok

		self.pos_start = self.tok.pos_start
		self.pos_end = self.tok.pos_end

	def __repr__(self):
		return f'{self.tok}'

class BinOpNode:
	def __init__(self, left_node, op_tok, right_node):
		self.left_node = left_node
		self.op_tok = op_tok
		self.right_node = right_node

		self.pos_start = self.left_node.pos_start
		self.pos_end = self.right_node.pos_end

	def __repr__(self):
		return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode: # damit wir ein + oder - vor einem Faktor (Integer oder Float) haben können.
	def __init__(self, op_tok, node):
		self.op_tok = op_tok
		self.node = node

		self.pos_start = self.op_tok.pos_start
		self.pos_end = node.pos_end

	def __repr__(self):
		return f'({self.op_tok}, {self.node})'

#########################################################################
# PARSE RESULT : Dies hilft, entweder einen Fehler oder den             #
# abstrakten Syntaxbaum (den Ausdrucksknoten) nach dem Parsen           #
# zurückzugeben                                                         #                           
#########################################################################

class ParseResult:
	def __init__(self):
		self.error = None
		self.node = None

	def register(self, res):
		if isinstance(res, ParseResult):
			if res.error: self.error = res.error
			return res.node

		return res

	def success(self, node):
		self.node = node
		return self

	def failure(self, error):
		self.error = error
		return self

###########################################################################
# PARSER : wird die Tokenliste durchlaufen, um verschiedene Knoten des    #
# Baumes (AST) zu erstellen                                               #
###########################################################################

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tok_idx = -1
		self.advance()

	def advance(self, ):
		self.tok_idx += 1
		if self.tok_idx < len(self.tokens):
			self.current_tok = self.tokens[self.tok_idx] # Wir können jederzeit neue Attribute erstellen, auch außerhalb des Konstruktors (hier self.current_tok)
		return self.current_tok

	def parse(self):
		res = self.expr()
		if not res.error and self.current_tok.type != TT_EOF: # Falls kein Fehler vorliegt, sollte self.current_tok.type auf TT_EOF stehen
			return res.failure(InvalidSyntaxError(
				self.current_tok.pos_start, self.current_tok.pos_end,
				"Expected '+', '-', '*' or '/'"
			))
		return res

	###################################

	def atom(self): # Ein Atom ist entweder ein Integer, ein Float oder ein Ausdruck in Klammern.
		res = ParseResult()
		tok = self.current_tok

		if tok.type in (TT_INT, TT_FLOAT): 
			res.register(self.advance())
			return res.success(NumberNode(tok))

		elif tok.type == TT_LPAREN: 
			res.register(self.advance())
			expr = res.register(self.expr())
			if res.error: return res
			if self.current_tok.type == TT_RPAREN:
				res.register(self.advance())
				return res.success(expr)
			
			else:
				return res.failure(InvalidSyntaxError(
					self.current_tok.pos_start, self.current_tok.pos_end,
					"Expected ')'"
				))

		return res.failure(InvalidSyntaxError(
			tok.pos_start, tok.pos_end,
			"Expected int, float, '+', '-' or '('"
		))

	def power(self):
		return self.bin_op(self.atom, (TT_POW, ), self.factor)

	def factor(self):
		res = ParseResult() # um am Ende entweder einen Knoten oder einen Fehler zu erhalten
		tok = self.current_tok

		if tok.type in (TT_PLUS, TT_MINUS): # Wir berücksichtigen den Fall, in dem ein Vorzeichen - oder + vor einem Faktor gefunden wird
			res.register(self.advance())
			factor = res.register(self.factor())
			if res.error: return res
			return res.success(UnaryOpNode(tok, factor))

		return self.power()

	def term(self):
		return self.bin_op(self.factor, (TT_MUL, TT_DIV))

	def expr(self):
		return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

	###################################

	def bin_op(self, func_a, ops, func_b=None):  
		if func_b == None:
			func_b = func_a
		
		res = ParseResult()
		left = res.register(func_a()) # Während der Konstruktion des linken Knotens wird das Attribut error von res aktualisiert, falls ein Fehler auftritt
		if res.error: return res

		while self.current_tok.type in ops:
			op_tok = self.current_tok
			res.register(self.advance())
			right = res.register(func_b())
			if res.error: return res
			left = BinOpNode(left, op_tok, right) # Jedes Mal, wenn der current_tok ein Operator ist, repräsentieren alle Ausdrücke, die davor kommen, 
												  # den linken Teil des BinOpNode, bis die gesamte Tokenliste durchlaufen wurde

		return res.success(left)





#######################################
# NODE PRINTER
#######################################

"""class PrintNode:
	@staticmethod
	def print_node(node, depth=0):
		indent = "  " * depth

		if isinstance(node, NumberNode):
			print(f"{indent}|__ {node.tok.value}")

		elif isinstance(node, BinOpNode):
			print(f"{indent}|__ {node.op_tok}")
			PrintNode.print_node(node.left_node, depth + 1)
			PrintNode.print_node(node.right_node, depth + 1)

		elif isinstance(node, UnaryOpNode):
			print(f"{indent}|__ {node.op_tok}")
			PrintNode.print_node(node.node, depth + 1)"""



#########################################################################
#   VALUES : values of Number                                           #
#########################################################################

class Number:
	def __init__(self, value):
		self.value = value
		self.set_pos()
		self.set_context()

	def set_pos(self, pos_start=None, pos_end=None):
		self.pos_start = pos_start
		self.pos_end = pos_end
		return self

	def set_context(self, context=None):
		self.context = context
		return self

	def added_to(self, other):
		if isinstance(other, Number):
			return Number(self.value + other.value).set_context(self.context), None

	def subbed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value - other.value).set_context(self.context), None

	def multed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value * other.value).set_context(self.context), None

	def dived_by(self, other):
		if isinstance(other, Number):
			if other.value == 0:
				return None, RTError(
					other.pos_start, other.pos_end,
					'Division by zero',
					self.context
				)

			return Number(self.value / other.value).set_context(self.context), None

	def powed_by(self, other):
		if isinstance(other, Number):
			return Number(self.value ** other.value).set_context(self.context), None

	def __repr__(self):
		return str(self.value)

#########################################################################
#   CONTEXT : Dies hilft, die Zeilen während der Ausführung zu          #
# verfolgen, sodass wir im Falle eines Fehlers den gesamten Verlauf vom #
# Anfang der Datei (Eingabe) bis zum Fehler zurückverfolgen können      #       
##########################################################################

class Context:
	def __init__(self, display_name, parent=None, parent_entry_pos=None):
		self.display_name = display_name
		self.parent = parent
		self.parent_entry_pos = parent_entry_pos






#########################################################################
# INTERMEDIATE CODE GENERATION :                                        #
# Dieser Teil hilft, Zwischenschritte oder Anweisungen aus dem          #
# abstrakten Syntaxbaum (AST) zu erzeugen.                              #         
######################################################################### 



class IntermediateInstruction:
	def __init__(self, opcode, atom=None):
		self.opcode = opcode
		self.atom = atom
		
		
		
	def __str__(self):
		if self.atom :
			return f"{self.opcode} {self.atom}"
		else:
			return f"{self.opcode}" 
		  
		
		

class IntermediateCodeGenerator:
	
	def __init__(self):
		self.instructions = []
		
	def generate(self, node, context):
		
		if isinstance(node, NumberNode):
			self.instructions.append(IntermediateInstruction(
				"PUSH", Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
			))
			
		elif isinstance(node, BinOpNode):
			self.generate(node.left_node, context)
			self.generate(node.right_node, context)
			
			if node.op_tok.type == TT_PLUS:
				self.instructions.append(IntermediateInstruction("ADD"))
			
			elif node.op_tok.type == TT_MINUS:
				self.instructions.append(IntermediateInstruction("SUB"))
				
			
			elif node.op_tok.type == TT_MUL:
				self.instructions.append(IntermediateInstruction("MUL"))
			
			elif node.op_tok.type == TT_DIV:
				self.instructions.append(IntermediateInstruction("DIV"))
			
			elif node.op_tok.type == TT_POW:
				self.instructions.append(IntermediateInstruction("POW"))
			
		elif isinstance(node, UnaryOpNode):
			self.generate(node.node, context)
			
			if node.op_tok.type == TT_MINUS:
				self.instructions.append(IntermediateInstruction("NEGATE"))
			else: pass
		
        
			
			





#########################################################################
# ABSTRAKTE STAPELMASCHINE (ABSTRACT STACK MACHINE):                    #
# Die abstrakte Stapelmaschine, die Berechnungen unter Verwendung von   # 
# Zwischenschritt-Anweisungen durchführen wird.                         #
#########################################################################

class AbstractStackMachine:
	def __init__(self):
		self.stack = []
		self.error = None

	def execute(self, instructions):
		
		
		
		for instruction in instructions:
			
			if instruction.opcode == "PUSH":
				self.stack.append(instruction.atom)
				
			elif instruction.opcode == "ADD":
				
				operand2 = self.stack.pop()
				operand1 = self.stack.pop()
				result, error = operand1.added_to(operand2)
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand1.pos_start, operand2.pos_end))
				
			elif instruction.opcode == "SUB":
				
				operand2 = self.stack.pop()
				operand1 = self.stack.pop()
				result, error = operand1.subbed_by(operand2)
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand1.pos_start, operand2.pos_end))
				
				
			elif instruction.opcode == "MUL":
				
				operand2 = self.stack.pop()
				operand1 = self.stack.pop()
				#print(f"Type operand1 : {type(operand1)}, Type operand2 {type(operand2)}")
				result, error = operand1.multed_by(operand2)
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand1.pos_start, operand2.pos_end))
				
			elif instruction.opcode == "DIV":
				
				operand2 = self.stack.pop()
				operand1 = self.stack.pop()
				result, error = operand1.dived_by(operand2)
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand1.pos_start, operand2.pos_end))
				
			elif instruction.opcode == "POW":
				
				operand2 = self.stack.pop()
				operand1 = self.stack.pop()
				result, error = operand1.powed_by(operand2)
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand1.pos_start, operand2.pos_end))
				
			elif instruction.opcode == "NEGATE":
				
				operand = self.stack.pop()
				result, error = operand.multed_by(Number(-1))
				
				if error:
					self.error = error
					break 
				else:
					self.stack.append(result.set_pos(operand.pos_start, operand.pos_end))
				
		if self.error: return None, self.error
		
		return self.stack[-1], None
	




#########################################################################
# RUN : Die Funktion, die hilft, das Programm auszuführen               #
######################################################################### 


def run(fn, text, line_number):
	# Generate tokens
	lexer = Lexer(fn, text, line_number)
	tokens, error = lexer.make_tokens()
	if error:
		return None, None, None, None, error
	
	# Generate AST
	parser = Parser(tokens)
	ast = parser.parse()
	#return ast.node, ast.error
	if ast.error:
		return None, None, None, None, ast.error
	
 	#Intermediate code generation
	context = Context('<program>')
	intermediate_instruction = IntermediateCodeGenerator()
	intermediate_instruction.generate(ast.node, context)
	intermediate_code = intermediate_instruction.instructions
 
	#return instructions, None
	abstractstackmachine = AbstractStackMachine()
	result, error = abstractstackmachine.execute(intermediate_code)
 	
	if error:
		return None, None, None, None, error
	else:
		return tokens, ast, intermediate_code, result, None, 
	 

