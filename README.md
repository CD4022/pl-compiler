# Project Description - Principles of Compiler Design
## Introduction
- In this project, we intend to design and implement a compiler for a programming language named PL, which is similar to the C language. The compiler consists of a lexical analyzer, syntactic analyzer, semantic analyzer, intermediate code generator and optimizer, and an assembly code generator and optimizer. A complete compiler receives a program written in a programming language as a text file and produces the equivalent assembly code.

- In this project, the design and implementation of the compiler do not produce assembly code, meaning it is not a complete compiler. The lexical analyzer extracts tokens from a program written in the PL programming language and sends these tokens to the syntactic analyzer, which, based on the grammar of the language, parses the tokens and constructs a parse tree using algorithms such as top-down and bottom-up parsing. If there is no error in the input program, the semantic analyzer executes the program and, in case of errors, issues error messages.

- A comprehensive report on how each part of the compiler is designed should be prepared. The compiler can be implemented in any language (e.g., C++, Java, Python). However, students must mention the source of each part of the compiler they implement. If they use artificial intelligence engines (e.g., Bing), they must mention the sources.

## Lexical Analyzer
1. *Keywords*
- The lexical analyzer identifies the following keywords in the PL language:
    * `if`
    * `else`
    * `for`
    * `return`
    * `int`
    * `bool`
    * `break`
    * `char`
    * `continue`
    * `true`
    * `flase`
    * `print`

2. *Identifiers*
- An identifier is a name for an entity in a programming language. In this language, entities include variables and functions. A variable is a sequence of memory locations with a name, and a function is an entity with a name that receives several inputs and performs certain operations, returning a value in some cases. Identifiers can contain letters, digits, and underscores but cannot start with a digit or an underscore and cannot be keywords.

3. *Punctuation Marks*
- The punctuation marks in this language are as follows:

    * Curly braces `{` and `}` are used for defining blocks.
    * Parentheses `(` and `)` are used for defining and calling functions and in arithmetic expressions.
    * Square brackets `[` and `]` are used for defining arrays.
    * Commas `,` are used for separating function parameters.
    * Semicolons `;` are used to terminate statements.

4. *Comments*
- Comments start with `//` and continue to the end of the line. However, comments are not sent to the syntactic analyzer but are listed by the lexical analyzer after extracting all tokens.

5. *Numeric Values*
- Numeric values can be `decimal` (base 10) or `hexadecimal` (base 16). Hexadecimal numbers start with `0x`. Negative numbers are indicated by a minus sign `-`.

6. *Characters and Strings*
- A character constant is represented by a single character enclosed in single quotes `'`. To represent an apostrophe within a character constant, use the backslash `\`. String constants are sequences of characters enclosed in double quotes `"`.

7. *Operators*
- Arithmetic operators include addition `+`, subtraction `-`, multiplication `*`, division `/`, and remainder `%`. Relational operators include `>`, `<`, `>=`, `<=`, `==`, and `!=`. Logical operators include `&&`, `||`, and `!`. The assignment operator is `=`.

8. *Whitespace*
- Whitespace includes space, newline `\n`, and tab `\t` characters and separates tokens.

9. *Token List*
- The following table lists the tokens for the PL language:

    * `Lexeme`         Token
    * `bool`           T_BOOL
    * `break`          T_BREAK
    * `char`           T_CHAR
    * `continue`       T_CONTINUE
    * `else`           T_ELSE
    * `false`          T_FALSE
    * `for`            T_FOR
    * `if`             T_IF
    * `int`            T_INT
    * `print`          T_PRINT
    * `return`         T_RETURN
    * `true`           T_TRUE
    * `+`              T_AOP_ADD
    * `-`              T_AOP_SUB
    * `*`              T_AOP_MUL
    * `/`              T_AOP_DIV
    * `%`              T_AOP_MOD
    * `<`              T_ROP_LT
    * `>`              T_ROP_GT
    * `<=`             T_ROP_LE
    * `>=`             T_ROP_GE
    * `==`             T_ROP_EQ
    * `!=`             T_ROP_NE
    * `&&`            T_LOP_AND
    * `||`             T_LOP_OR
    * `!`              T_LOP_NOT
    * `=`              T_ASSIGN
    * `(`              T_LP
    * `)`              T_RP
    * `{`              T_LC
    * `}`              T_RC
    * `[`              T_LB
    * `]`              T_RB
    * `;`              T_SEMICOLON
    * `,`              T_COMMA
    * `variable or function names` T_ID
    * `decimal integers` T_DECIMAL
    * `hexadecimal integers` T_HEXADECIMAL
    * `constant strings "[string]"` T_STRING
    * `constant characters '[character]'` T_CHARACTER
    * `//[string]\n` T_COMMENT
    * `whitespace (newline, tab, and space characters)` T_WHITESPACE


## Syntax Analyzer
- In this part of the project, we want to design and implement a syntactic analyzer for the PL programming language. The syntactic analyzer receives a sequence of tokens from the lexical analyzer and, if there are no syntactic errors in the input program, constructs a parse tree. Otherwise, it prints the error messages. The simplest method to implement the syntactic analyzer is to use a predictive parser. If the input is erroneous, the compiler should use error recovery techniques.

1. *Variables and Data Types*
- The language has three primary data types: int, char, and bool. Variables can be defined with these data types. Arrays can also be defined with a specific size and data type using square brackets [].

2. *Expressions*
- Expressions are combinations of variables, constants, and operators. The following types of expressions are allowed in the PL language:

    * Arithmetic expressions: `a + b`, `c - d`, `e * f`, `g / h`, `i % j`
    * Relational expressions: `a < b`, `c > d`, `e <= f`, `g >= h`, `i == j`, `k != l`
    * Logical expressions: `a && b`, `c || d`, `!e`

3. *Statements*
- The following types of statements are allowed in the PL language:

    * Assignment statements: `variable = expression;`
    * Conditional statements: `if (expression) { statement } else { statement }`
    * Loop statements: `for (initialization; condition; increment) { statement }`
    * Function calls: `function_name(parameters);`
    * Return statements: `return expression;`

## Semantic Analyzer

- In this part of the project, we want to design and implement a semantic analyzer for the PL programming language. The semantic analyzer performs checks such as type checking, scope resolution, and function verification. It receives a parse tree from the syntactic analyzer and generates a semantic tree if there are no semantic errors in the input program. The semantic tree is created using the rules of semantic analysis.

* Each identifier must be declared before use. An identifier can be a `variable` or a `function`.
* Each scope starts with a specific block. A scope can have multiple sub-scopes. A block begins with an opening curly brace `{` and ends with a closing curly brace `}`. If a new block is started within another block, it is considered a sub-scope of the outer block. Scopes define the visibility and lifetime of variables.
* The language has three basic data types: `int`, `char`, and `bool`.
* The operands of arithmetic operators must be of type `int`, and the operands of logical operators must be of type `bool`.
* The index of an array must be of type `int` and greater than or equal to zero.
* The type of the conditional expression in an `if` statement must be `bool`.
* The `main` function must have no parameters, and its `return` type must be `int`.
* Function calls must match the number and types of parameters defined in the function's declaration.
* In an assignment statement, the type of the left-hand side must match the type of the right-hand side. If there are nested assignments, each left-hand side must match the type of the right-hand side.
* The type of the expression in a return statement must match the return type of the function.
