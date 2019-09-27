import sys

# STATE TYPES
ST_OPERATOR = 0  # "OPERATOR"
ST_SEPARATOR = 1  # "SEPARATOR"
ST_IDENTIFIER = 2  # "IDENTIFIER"
ST_KEYWORD = 3  # "KEYWORD"
ST_INT = 4  # "INT"
ST_REAL = 5  # "REAL"
ST_COMMENT = 6  # "!"
ST_DECIMAL = 7  # "DECIMAL"
ST_SPACE = 8  # "SPACE"
ST_ERROR = 9  # "ERROR"

# This array is used to convert the state type to a token
get_token_string = ["OPERATOR", "SEPARATOR", "IDENTIFIER",
                    "KEYWORD", "INT", "REAL", "COMMENT", "DECIMAL", "SPACE", "ERROR"]

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
    ST_INT: {
        CT_ALPHA: ST_ERROR,
        CT_DIGIT: ST_INT,
        CT_DECIMAL: ST_DECIMAL,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_REAL: {
        CT_ALPHA: ST_ERROR,
        CT_DIGIT: ST_REAL,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_DECIMAL: {
        CT_ALPHA: ST_ERROR,
        CT_DIGIT: ST_REAL,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_ERROR,
        CT_OPERATOR: ST_ERROR,
        CT_SEPARATOR: ST_ERROR,
        CT_BANG: ST_COMMENT
    },
    ST_SPACE: {
        CT_ALPHA: ST_KEYWORD,
        CT_DIGIT: ST_INT,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_SEPARATOR: {
        CT_ALPHA: ST_KEYWORD,
        CT_DIGIT: ST_INT,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_ERROR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_OPERATOR: {
        CT_ALPHA: ST_KEYWORD,
        CT_DIGIT: ST_INT,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_ERROR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_KEYWORD: {
        CT_ALPHA: ST_KEYWORD,
        CT_DIGIT: ST_IDENTIFIER,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_IDENTIFIER,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_IDENTIFIER: {
        CT_ALPHA: ST_IDENTIFIER,
        CT_DIGIT: ST_IDENTIFIER,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_IDENTIFIER,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_COMMENT
    },
    ST_COMMENT: {
        CT_ALPHA: ST_COMMENT,
        CT_DIGIT: ST_COMMENT,
        CT_DECIMAL: ST_COMMENT,
        CT_DOLLAR: ST_COMMENT,
        CT_SPACE: ST_COMMENT,
        CT_OPERATOR: ST_COMMENT,
        CT_SEPARATOR: ST_COMMENT,
        CT_BANG: ST_SPACE
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
    current_state = ST_SPACE

    with open(filename) as f:
        while True:
            char = f.read(1)

            char_type = get_char_type(char)

            new_state = transition_table[current_state][char_type]

            # Exit on an error state
            if(new_state == ST_ERROR):
                print("ILLEGAL TOKEN: ", token.strip() + char)
                token = ""
                continue

            if(current_state != new_state):  # If the state has changed....
                # If the current state was just a space or a comment we do not want to append them to the token.
                # Instead we start a fresh token using the new char
                if(current_state == ST_SPACE or current_state == ST_COMMENT):
                    token = char

                # If there is a state change and we are changing into a decimal point or out of a decimal point
                # we want to concat that to the current token
                elif(current_state == ST_DECIMAL or new_state == ST_DECIMAL):
                    token = token + char

                # If there is a state change and the new state is an identifier, then we are transitioning
                # from a keyword to an identifier, so just concat the char to the token.
                elif(new_state == ST_IDENTIFIER):
                    token = token + char

                # If any other state change occurs...
                else:
                    # If we're current in the keyword state, make sure it is in the keyword list,
                    # Otherwise, it's an identifier.
                    if(current_state == ST_KEYWORD and token not in KEYWORDS):
                        tokens.append((get_token_string[ST_IDENTIFIER], token))

                    # All other cases append the token that we've built.
                    else:
                        tokens.append((get_token_string[current_state], token))

                    # start a new token with the new char
                    token = char

            # If it's not a state change, append the char to the token and continue.
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
