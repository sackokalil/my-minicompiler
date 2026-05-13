\# Mini Compiler for Arithmetic Expressions



A mini compiler/interpreter project implemented in Python for arithmetic expression computation.



The project was developed in the context of Compiler Construction (Compilerbau) and demonstrates the complete compilation pipeline:



\- lexical analysis

\- parsing

\- abstract syntax tree generation

\- intermediate code generation

\- execution using an abstract stack machine

\- runtime and syntax error handling



The compiler supports arithmetic expressions with operator precedence and parentheses.



\---



\# Project Overview



This project implements the fundamental concepts of compiler construction.



The workflow includes:



\- tokenization using a Lexer

\- parsing using grammar rules

\- AST (Abstract Syntax Tree) construction

\- intermediate instruction generation

\- execution using a stack-based virtual machine

\- detailed syntax/runtime error reporting



\---



\# Features



\- Integer and float support

\- Arithmetic operations:

&#x20; - Addition

&#x20; - Subtraction

&#x20; - Multiplication

&#x20; - Division

&#x20; - Power operator

\- Unary operators (`+`, `-`)

\- Parentheses support

\- Operator precedence handling

\- Abstract Syntax Tree generation

\- Intermediate code generation

\- Stack machine execution

\- Detailed lexical, syntax, and runtime errors

\- File input support

\- Interactive shell mode



\---



\# Supported Operators



```text

\+

\-

\*

/

^

()

```



\---



\# Grammar



The parser is based on the following grammar:



```text

expr    : term ((PLUS|MINUS) term)\*



term    : factor ((MUL|DIV) factor)\*



factor  : (PLUS|MINUS) factor

&#x20;       : power



power   : atom (POW factor)\*



atom    : INT|FLOAT

&#x20;       : LPAREN expr RPAREN

```



The grammar ensures correct operator precedence and associativity.



\---



\# Project Structure



```text

.

├── basic1.py

├── shell1.py

├── strings\_with\_arrows.py

├── grammar.txt

├── how\_it\_works.txt

├── exemple\_expression.txt

└── README.md

```



\---



\# Compiler Pipeline



\## 1. Lexer



The Lexer scans the input character by character and transforms the text into tokens.



Example tokens:



```text

TT\_INT

TT\_FLOAT

TT\_PLUS

TT\_MINUS

TT\_MUL

TT\_DIV

TT\_POW

TT\_LPAREN

TT\_RPAREN

```



Implemented inside:



```text

basic1.py

```



\---



\## 2. Parser



The Parser reads the token list and builds an Abstract Syntax Tree (AST).



The parser handles:



\- operator precedence

\- unary operations

\- nested expressions

\- parentheses



AST nodes include:



\- NumberNode

\- BinOpNode

\- UnaryOpNode



\---



\# Example AST



Expression:



```text

(1+3) \* 56 - 9

```



AST representation:



```text

(((TT\_INT:1, TT\_PLUS, TT\_INT:3), TT\_MUL, TT\_INT:56), TT\_MINUS, TT\_INT:9)

```



\---



\# Intermediate Code Generation



The AST is transformed into intermediate instructions.



Example instructions:



```text

PUSH 5

PUSH 3

ADD

PUSH 2

MUL

```



Supported instructions:



\- PUSH

\- ADD

\- SUB

\- MUL

\- DIV

\- POW

\- NEGATE



\---



\# Abstract Stack Machine



The generated intermediate instructions are executed using an Abstract Stack Machine.



The machine:



\- creates a stack

\- pushes temporary values

\- executes operations

\- returns the final computed result



The execution model is similar to a virtual machine.



\---



\# Error Handling



The compiler supports several types of errors:



\## Lexical Errors



Example:



```text

2\*(52-10\*3)$25

```



Result:



```text

Illegal Character Error

```



\---



\## Syntax Errors



Example:



```text

2+(3\*(52-10\*3))25

```



Result:



```text

Invalid Syntax Error

```



\---



\## Runtime Errors



Example:



```text

2\*56\*(25+3)-(2\*3)\*2-6^2/0

```



Result:



```text

Division by zero

```



The project displays detailed error positions using arrows.



\---



\# Interactive Shell



The project includes an interactive shell interface.



Run:



```bash

python shell1.py

```



The shell allows:



\- direct expression input

\- file-based input

\- multiline processing

\- automatic error reporting



\---



\# Example Expressions



```text

2\*5+25-(3-5)\*2-(25+15)-2\*56\*(25+3)-(2\*3)\*2-6^2

```



```text

\-2\*56\*(25+3)-(2\*3)\*2-6^2

```



```text

2\*56\*(25+3)-(2\*3)\*2-6^2/0

```



\---



\# Technologies Used



\- Python

\- Recursive Descent Parsing

\- Stack Machine Execution

\- Compiler Construction Concepts



\---



\# Concepts Demonstrated



\- Lexer

\- Parser

\- AST (Abstract Syntax Tree)

\- Recursive Descent Parsing

\- Intermediate Representation

\- Virtual Stack Machine

\- Runtime Error Handling

\- Context Tracking

\- Tokenization



\---



\# Author



Kalil Sacko



Master Student in Computer Science  

Hochschule Bochum



\---



\# Notes



\- The project was developed for learning compiler construction concepts.

\- The parser is implemented manually using recursive descent parsing.

\- The compiler generates intermediate instructions before execution.

\- Error tracing includes exact line and column information.

