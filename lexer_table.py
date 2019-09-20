transition_table = {
    "INT": {
        "ALPHA": "ERROR",
        "DIGIT": "INT",
        "DECIMAL": "DECIMAL",
        "$": "ERROR",
        "SPACE": "SPACE",
        "OPERATOR": "OPERATOR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "REAL": {
        "ALPHA": "ERROR",
        "DIGIT": "REAL",
        "DECIMAL": "ERROR",
        "$": "ERROR",
        "SPACE": "SPACE",
        "OPERATOR": "OPERATOR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "DECIMAL": {
        "ALPHA": "ERROR",
        "DIGIT": "REAL",
        "DECIMAL": "ERROR",
        "$": "ERROR",
        "SPACE": "ERROR",
        "OPERATOR": "ERROR",
        "SEPARATOR": "ERROR",
        "!": "!"
    },
    "SPACE": {
        "ALPHA": "KEYWORD",
        "DIGIT": "INT",
        "DECIMAL": "ERROR",
        "$": "ERROR",
        "SPACE": "SPACE",
        "OPERATOR": "OPERATOR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "SEPARATOR": {
        "ALPHA": "KEYWORD",
        "DIGIT": "INT",
        "DECIMAL": "ERROR",
        "$": "ERROR",
        "SPACE": "SPACE",
        "OPERATOR": "ERROR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "OPERATOR": {
        "ALPHA": "KEYWORD",
        "DIGIT": "INT",
        "DECIMAL": "ERROR",
        "$": "ERROR",
        "SPACE": "SPACE",
        "OPERATOR": "ERROR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "KEYWORD": {
        "ALPHA": "KEYWORD",
        "DIGIT": "IDENTIFIER",
        "DECIMAL": "ERROR",
        "$": "IDENTIFIER",
        "SPACE": "SPACE",
        "OPERATOR": "OPERATOR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "IDENTIFIER": {
        "ALPHA": "IDENTIFIER",
        "DIGIT": "IDENTIFIER",
        "DECIMAL": "ERROR",
        "$": "IDENTIFIER",
        "SPACE": "SPACE",
        "OPERATOR": "OPERATOR",
        "SEPARATOR": "SEPARATOR",
        "!": "!"
    },
    "!": {
        "ALPHA": "!",
        "DIGIT": "!",
        "DECIMAL": "!",
        "$": "!",
        "SPACE": "!",
        "OPERATOR": "!",
        "SEPARATOR": "!",
        "!": "SPACE"
    },
}


# TOKEN TYPES
TT_OPERATOR = "OPERATOR"
TT_SEPARATOR = "SEPARATOR"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"
TT_INT = "INT"
TT_REAL = "REAL"
TT_COMMENT = "!"
TT_DECIMAL = "DECIMAL"
TT_SPACE = "SPACE"

# CHARACTER TYPES
CT_SPACE = "SPACE"
CT_DIGIT = "DIGIT"
CT_COMMENT = "!"
CT_DECIMAL = "DECIMAL"
CT_DOLLAR = "$"
CT_OPERATOR = "OPERATOR"
CT_SEPARATOR = "SEPARATOR"

# GROUP TYPE DEFINITIONS
SEPARATORS = "'()}{[],.:;!"
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "if", "else", "then",
            "endif", "while", "whileend",
            "do", "doend", "for", "forend", "input",
            "output", "and", "or", "function"]


def get_char_type(char):
    char_type = None

    if(char.isspace() or char == ''):
        char_type = 'SPACE'
    elif (char.isdigit()):
        char_type = 'DIGIT'
    elif ('!' == char):
        char_type = "!"
    elif('.' == char):
        char_type = 'DECIMAL'
    elif ('$' == char):
        char_type = '$'
    elif (char in OPERATORS):
        char_type = 'OPERATOR'
    elif (char in SEPARATORS):
        char_type = 'SEPARATOR'
    elif (char.isalpha()):
        char_type = 'ALPHA'

    return char_type


# Begin lexer
token = ""
tokens = []
current_state = 'SPACE'

with open('test.txt') as f:
    while True:
        char = f.read(1)

        char_type = get_char_type(char)

        new_state = transition_table[current_state][char_type]

        # Exit on an error state
        if(new_state == "ERROR"):
            print("ILLEGAL TOKEN: ", token.strip() + char)
            break

        if(current_state != new_state):
            if(current_state == TT_SPACE or current_state == TT_COMMENT):
                token = char
            elif(current_state == TT_DECIMAL or new_state == TT_DECIMAL):  # INT -> DECIMAL -> REAL
                token = token + char
            elif(new_state == TT_IDENTIFIER):  # KEYWORD -> IDENTIFIER
                token = token + char
            else:
                if(current_state == TT_KEYWORD and token not in KEYWORDS):
                    tokens.append((TT_IDENTIFIER, token))
                else:
                    tokens.append((current_state, token))

                token = char
        else:
            token = token + char

        current_state = new_state

        # If done reading the file...
        if not char:
            # print("End of file")
            break

for token in tokens:
    print(token[0], "\t", token[1])
