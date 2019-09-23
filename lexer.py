import sys

# TOKEN TYPES
TT_OPERATOR = 0  # "OPERATOR"
TT_SEPARATOR = 1  # "SEPARATOR"
TT_IDENTIFIER = 2  # "IDENTIFIER"
TT_KEYWORD = 3  # "KEYWORD"
TT_INT = 4  # "INT"
TT_REAL = 5  # "REAL"
TT_COMMENT = 6  # "!"
TT_DECIMAL = 7  # "DECIMAL"
TT_SPACE = 8  # "SPACE"
TT_ERROR = 9  # "ERROR"

get_token_string = ["OPERATOR", "SEPARATOR", "IDENTIFIER",
                    "KEYWORD", "INT", "REAL", "!", "DECIMAL", "SPACE", "ERROR"]

# CHARACTER TYPES
CT_ALPHA = 0  # "ALPHA"
CT_SPACE = 1  # "SPACE"
CT_DIGIT = 2  # "DIGIT"
CT_BANG = 3  # "!"
CT_DECIMAL = 4  # "DECIMAL"
CT_DOLLAR = 5  # "$"
CT_OPERATOR = 6  # "OPERATOR"
CT_SEPARATOR = 7  # "SEPARATOR"


def get_char_type(char):
    char_type = None

    if(char.isspace() or char == ''):
        char_type = CT_SPACE
    elif (char.isdigit()):
        char_type = CT_DIGIT
    elif ('!' == char):
        char_type = CT_BANG
    elif('.' == char):
        char_type = CT_DECIMAL
    elif ('$' == char):
        char_type = CT_DOLLAR
    elif (char in OPERATORS):
        char_type = CT_OPERATOR
    elif (char in SEPARATORS):
        char_type = CT_SEPARATOR
    elif (char.isalpha()):
        char_type = CT_ALPHA

    return char_type


transition_table = {
    TT_INT: {
        CT_ALPHA: TT_ERROR,
        CT_DIGIT: TT_INT,
        CT_DECIMAL: TT_DECIMAL,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_OPERATOR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_REAL: {
        CT_ALPHA: TT_ERROR,
        CT_DIGIT: TT_REAL,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_OPERATOR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_DECIMAL: {
        CT_ALPHA: TT_ERROR,
        CT_DIGIT: TT_REAL,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_ERROR,
        CT_OPERATOR: TT_ERROR,
        CT_SEPARATOR: TT_ERROR,
        CT_BANG: TT_COMMENT
    },
    TT_SPACE: {
        CT_ALPHA: TT_KEYWORD,
        CT_DIGIT: TT_INT,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_OPERATOR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_SEPARATOR: {
        CT_ALPHA: TT_KEYWORD,
        CT_DIGIT: TT_INT,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_ERROR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_OPERATOR: {
        CT_ALPHA: TT_KEYWORD,
        CT_DIGIT: TT_INT,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_ERROR,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_ERROR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_KEYWORD: {
        CT_ALPHA: TT_KEYWORD,
        CT_DIGIT: TT_IDENTIFIER,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_IDENTIFIER,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_OPERATOR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_IDENTIFIER: {
        CT_ALPHA: TT_IDENTIFIER,
        CT_DIGIT: TT_IDENTIFIER,
        CT_DECIMAL: TT_ERROR,
        CT_DOLLAR: TT_IDENTIFIER,
        CT_SPACE: TT_SPACE,
        CT_OPERATOR: TT_OPERATOR,
        CT_SEPARATOR: TT_SEPARATOR,
        CT_BANG: TT_COMMENT
    },
    TT_COMMENT: {
        CT_ALPHA: TT_COMMENT,
        CT_DIGIT: TT_COMMENT,
        CT_DECIMAL: TT_COMMENT,
        CT_DOLLAR: TT_COMMENT,
        CT_SPACE: TT_COMMENT,
        CT_OPERATOR: TT_COMMENT,
        CT_SEPARATOR: TT_COMMENT,
        CT_BANG: TT_SPACE
    },
}


# GROUP TYPE DEFINITIONS
SEPARATORS = "'()}{[],.:;!"
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "if", "else", "then",
            "endif", "while", "whileend",
            "do", "doend", "for", "forend", "input",
            "output", "and", "or", "function"]


def lexer(filename):
    token = ""
    tokens = []
    current_state = TT_SPACE

    with open(filename) as f:
        while True:
            char = f.read(1)

            char_type = get_char_type(char)

            new_state = transition_table[current_state][char_type]

            # Exit on an error state
            if(new_state == TT_ERROR):
                print("ILLEGAL TOKEN: ", token.strip() + char)
                break

            if(current_state != new_state):
                if(current_state == TT_SPACE or current_state == TT_COMMENT):
                    token = char
                elif(current_state == TT_DECIMAL or new_state == TT_DECIMAL):
                    token = token + char
                elif(new_state == TT_IDENTIFIER):  # KEYWORD -> IDENTIFIER
                    token = token + char
                else:
                    if(current_state == TT_KEYWORD and token not in KEYWORDS):
                        tokens.append((get_token_string[TT_IDENTIFIER], token))
                    else:
                        tokens.append((get_token_string[current_state], token))

                    token = char
            else:
                token = token + char

            current_state = new_state

            # If done reading the file...
            if not char:
                # print("End of file")
                break
    return tokens


if __name__ == "__main__":
    # To lex a file, please pass the filename as the first argument
    # Example usage: python3 lexer.py [filename]
    filename = sys.argv[1]

    tokens = lexer(filename)

    print("TOKENS\t\t\tLexemes\n")
    for token in tokens:
        print(token[0], "\t=\t", token[1])
