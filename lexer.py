
# TOKEN TYPES
TT_OPERATOR = "OPERATOR"
TT_SEPARATOR = "SEPARATOR"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_INT = "INT"
TT_REAL = "REAL"

# STATE MODES
SM_SPACE = "SPACE"
SM_OPERATOR = "OPERATOR"
SM_SEPARATOR = "SEPARATOR"
SM_IDENTIFIER = "IDENTIFIER"
SM_KEYWORD = "KEYWORD"
SM_INT = "INT"
SM_REAL = "REAL"
SM_DECIMAL = "DECIMAL"


# CONSTANTS
SEPARATORS = "'()\{\}[],.:;! "
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "if", "else", "then",
            "endif", "while", "whileend",
            "do", "doend", "for", "forend", "input",
            "output", "and", "or", "function"]

# Begin lexer
token = ""
tokens = []
mode = SM_SPACE

with open('test.txt') as f:
    while True:
        char = f.read(1)
        # print(mode, char, token)
        if not char:
            # print("End of file")
            break

        if(mode == SM_SPACE):
            token = char
            if(char.isspace()):
                mode = SM_SPACE
            elif(char.isalpha()):
                mode = SM_KEYWORD
            elif(char.isdigit()):
                mode = SM_INT
            elif(char in SEPARATORS):
                mode = SM_SEPARATOR
            elif(char in OPERATORS):
                mode = SM_OPERATOR
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_SEPARATOR or mode == SM_OPERATOR):
            tokens.append((mode, token))  # Appends the operator or separator
            token = char  # Starts a new token with the new character
            if (char.isspace()):
                mode = SM_SPACE
            elif (char.isdigit()):
                mode = SM_INT
            elif (char.isalpha()):
                mode = SM_KEYWORD
            elif (char in SEPARATORS):
                mode = SM_SEPARATOR
            elif (char in OPERATORS):
                mode = SM_OPERATOR
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_INT):
            if (char == '.'):
                token = token + char
                mode = SM_DECIMAL
            elif (char.isdigit()):
                token = token + char
                mode = SM_INT  # Can remove
            elif(char in SEPARATORS):
                tokens.append((TT_INT, token))
                token = char
                mode = SM_SEPARATOR
            elif (char in OPERATORS):
                tokens.append((TT_INT, token))
                token = char
                mode = SM_OPERATOR
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_DECIMAL):
            if (char.isdigit()):
                token = token + char
                mode = SM_REAL  # Can remove
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_REAL):
            if (char.isdigit()):
                token = token + char
                mode = SM_REAL  # can remove
            elif(char.isspace()):
                tokens.append((TT_REAL, token))
                token = char
                mode = SM_SPACE
            elif(char in SEPARATORS):
                tokens.append((TT_REAL, token))
                token = char
                mode = SM_SEPARATOR
            elif (char in OPERATORS):
                tokens.append((TT_REAL, token))
                token = char
                mode = SM_OPERATOR
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_KEYWORD):
            if(char.isalpha()):
                token = token + char
            elif(char.isdigit() or char == '$'):
                token = token + char
                mode = SM_IDENTIFIER
            elif(char.isspace()):
                if(token in KEYWORDS):
                    tokens.append((TT_KEYWORD, token))
                else:
                    tokens.append((TT_IDENTIFIER, token))
                token = char
                mode = SM_SPACE
            elif(char in SEPARATORS):
                if(token in KEYWORDS):
                    tokens.append((TT_KEYWORD, token))
                else:
                    tokens.append((TT_IDENTIFIER, token))
                token = char
                mode = SM_SEPARATOR
            elif(char in OPERATORS):
                if(token in KEYWORDS):
                    tokens.append((TT_KEYWORD, token))
                else:
                    tokens.append((TT_IDENTIFIER, token))
                token = char
                mode = SM_OPERATOR
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

        elif(mode == SM_IDENTIFIER):
            if(char.isalpha() or char.isdigit() or char == '$'):
                token = token + char
                mode = SM_IDENTIFIER
            else:
                #
                # Invalid syntax
                #
                print('Syntax Error')
                pass

    if(mode != SM_DECIMAL and mode != SM_SPACE):
        tokens.append((mode, token))

print("{:20}{:15}".format("Token", "Lexeme"))
print("-"*35)

for token in tokens:
    print("{:20}{:15}".format(token[0], token[1]))
