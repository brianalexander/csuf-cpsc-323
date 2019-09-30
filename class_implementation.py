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
                    "KEYWORD", "INT", "REAL", "COMMENT",
                    "DECIMAL", "SPACE", "ERROR"]

# CHARACTER TYPES
CT_ALPHA = 0  # "ALPHA"
CT_SPACE = 1  # "SPACE"
CT_DIGIT = 2  # "DIGIT"
CT_BANG = 3  # "!"
CT_DECIMAL = 4  # "DECIMAL"
CT_DOLLAR = 5  # "$"
CT_OPERATOR = 6  # "OPERATOR"
CT_SEPARATOR = 7  # "SEPARATOR"

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
        CT_BANG: ST_ERROR,
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
        CT_OPERATOR: ST_OPERATOR,
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
    ST_ERROR: {
        CT_ALPHA: ST_ERROR,
        CT_DIGIT: ST_ERROR,
        CT_DECIMAL: ST_ERROR,
        CT_DOLLAR: ST_ERROR,
        CT_SPACE: ST_SPACE,
        CT_OPERATOR: ST_OPERATOR,
        CT_SEPARATOR: ST_SEPARATOR,
        CT_BANG: ST_ERROR,
    }
}

# GROUP TYPE DEFINITIONS
SEPARATORS = "'()}{[],.:;"
OPERATORS = "*+-=/><%"
KEYWORDS = ["int", "float", "bool", "if", "else", "then",
            "endif", "while", "whileend",
            "do", "doend", "for", "forend", "input",
            "output", "and", "or", "function"]


class Lexer:
    def __init__(self, path):
        self._file = open(path)
        self.line_number = 1
        self.token = ""
        self.current_state = ST_SPACE

    def get_char_type(self, char):
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

    def get_token(self):
        while(True):
            char = self._file.read(1)

            if(char == '\n'):
                self.line_number = self.line_number + 1

            char_type = self.get_char_type(char)

            new_state = transition_table[self.current_state][char_type]

            # If the state has changed....
            if(self.current_state != new_state):
                # If the current state was just a space or a comment we do not want to append them to the token.
                # Instead we start a fresh token using the new char
                if(self.current_state == ST_SPACE or self.current_state == ST_COMMENT):
                    self.token = char

                # If there is a state change and we are changing into a decimal point or out of a decimal point
                # we want to concat that to the current token
                elif(self.current_state == ST_DECIMAL or new_state == ST_DECIMAL):
                    self.token = self.token + char

                # If there is a state change and the new state is an identifier, then we are transitioning
                # from a keyword to an identifier, so just concat the char to the token.
                elif(new_state == ST_IDENTIFIER):
                    self.token = self.token + char

                # If there is a state change and we have entered an error state
                # the previous token is part of that error.  Append the new char
                # and continue building the illegal token
                elif(new_state == ST_ERROR):
                    self.token = self.token + char

                # If any other state change occurs...
                else:
                    return_token = self.token.strip()
                    return_state = self.current_state

                    # start a new token with the new char
                    self.current_state = new_state
                    self.token = char

                    # If we're current in the keyword state, make sure it is in the keyword list,
                    # Otherwise, it's an identifier.
                    if(return_state == ST_KEYWORD and return_token not in KEYWORDS):
                        return (get_token_string[ST_IDENTIFIER], return_token)

                    # If we are exiting an error state, append the illegal token to our
                    # illegal token dictionary with the line number where it occurred
                    elif(return_state == ST_ERROR):
                        return ("ERROR: "+str(self.line_number), return_token)

                    # All other cases append the token that we've built.
                    else:
                        return (get_token_string[return_state], return_token)

            # If it's not a state change, append the char to the token and continue.
            else:
                self.token = self.token + char

            self.current_state = new_state

            # If done reading the file...
            if not char:
                # print("End of file")
                return None


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Please specify a file path to lex as the first argument.")
        sys.exit()

    # To lex a file, please pass the path as the first argument
    # Example usage: python3 lexer.py [path]
    path = sys.argv[1]
    lexer = Lexer(path)

    print("TOKENS\t\t\tLexemes")
    while True:
        token = lexer.get_token()
        if(token is None):
            break
        print("{0:<10}\t\t{1}".format(token[0], token[1]))
