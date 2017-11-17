# By Robert Chung
# HW for CSC 3310 - Concepts in Programming Languages
# Dr. Arias
# Lexer2.py
# This program should take a program written in Mini-Pascal and output the
#   Tokens and Lexemes into a new file.
# EXTRA CREDIT

# QUESTIONS:
# 1) Do we exit from program if we find a syntax error? Or do we keep going?
# 2) Example has different names for INTEGER: (INT) and PLUS: (ADD); does this matter?
# 3) How do you want us to format the output (spaces and stuff)
# 4) String token?? the ':' after a string in one of your example programs
# 5) You indicate that the quote should be a token, but it's never printed in any example programs.
#       Do you want us to print "QUOTE" when we encounter a quote, or just take it as a string?

# TODO
# 1) The last semicolon  -- done
# 2) Put it into an actual file instead of just printing -- done
# 3) Check program with tests (Faults)
# 4) Extra credit?
# 5) Think about more cases where things would be wrong (relates to #3 todo) -- done
# 6) Add comments -- done
# 7) Count number of tokens and stuff to print out to file
        # WHAT CONSTITUTES WHEN TO INCREASE COUNT WTF
# 8) Put the stuff you already encountered into a lookup table

import sys

miniPascalLetters = (
                     'a', 'b', 'c', 'd', 'e', 'f', 'e', 'g', 'h', 'i', 'j',
                     'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                     'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
                     'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
                     'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
                     )
miniPascalDigits = (
                    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
                   )
miniPascalOtherTokens = {
                         ';': "SEMICOLON", '+': "PLUS", '-': "MINUS",
                         '*': "TIMES", '=': "EQUALS", '(': "LPAREN",
                         ')': "RPAREN", "<>": "NOTEQUAL", '<': "LTHAN",
                         '>': "GRTHAN", "<=": "GROREQ", ">=": "LOREQ",
                         '[': "LBRACK", ']': "RBRACK", ":=": "ASSIGN",
                         '.': "PERIOD", ',': "COMMA", ':': "COLON",
                         "..": "RANGE", "div": "DIV", "or": "OR", "and": "AND",
                         "not": "NOT", "if": "IF", "then": "THEN",
                         "else": "ELSE", "of": "OF", "while": "WHILE",
                         "do": "DO", "begin": "BEGIN", "end": "END",
                         "read": "READ", "write": "WRITE", "var": "VAR",
                         "array": "ARRAY", "procedure": "PROCEDURE",
                         "program": "PROGRAM"
                         }
miniPascalIdentifiers = (
                         "integer", "Boolean", "true", "false"
                        )

# Global file
f = ""
f_out = ""

# Global characters, tokens, and lexemes
ch = " "
token = ""
lexeme = ""
tokenCount = 0


def main():
    global f
    global f_out

    # ----------------------------------------------------------------- #
    #                   ======= FILE OPENING =======                    #
    #                      Opening Input File
    inputFile = sys.argv[1]
    try:
        f = open(inputFile, 'r')
    except IOError:
        print "Unable to open the file you specificed! Please try again."
        return
    # ----------------------------------------------------------------- #
    #                Opening Output File for writing
    outputFile = inputFile.split('.')[0] + ".out"
    try:
        f_out = open(outputFile, 'w')
    except IOError:
        print "Error creating new file for writing"
        return
    # ================================================================= #

    # Actual lex time now
    print "Processing input file ", inputFile
    while ch != "":
        lex()
    print tokenCount, " tokens produced"
    print "Result in file " + outputFile

    f.close()
    f_out.close()


def getNextChar():
    global ch
    global f

    # process the next character if its not EOF
    if ch != "":
        ch = f.read(1)


def getNextNonWhiteSpace():
    global ch
    global f

    while ch == " " or ch == '\n' or ch == '\t':
        getNextChar()


def lex():
    global ch
    global f_out

    getNextNonWhiteSpace()
    if ch in miniPascalLetters:
        handleLetters()
    elif ch == '\'':
        handleCharConstant()
    elif ch in miniPascalOtherTokens:
        handleOtherTokens()
    elif ch in miniPascalDigits:
        handleIntegerConstant()
    elif ch == "":
        return
    else:
        f_out.write("SYNTAX ERROR: Character not recognized!\n")
        getNextChar()


def handleLetters():
    global ch
    global token
    global lexeme
    global tokenCount
    global f_out

    token = "ID"
    lexeme += ch
    getNextChar()

    # Loop until character isn't recognized by letter/digit
    #   add to current lexeme if it is recognized
    while ch in miniPascalLetters or ch in miniPascalDigits:
        lexeme += ch

        # If you encounter a reserved word
        if lexeme in miniPascalOtherTokens:
            token = miniPascalOtherTokens[lexeme]
            getNextChar()
            lexeme += ch

            # Check to see if its standalone reserved word or if they used
            #   something like beginWord (begin is reserved but not beginWord)
            if ch == ' ' or                   \
               ch == '\n' or                  \
               ch == '\t' or                  \
               ch in miniPascalOtherTokens:
                f_out.write(token + '\n')
                lexeme = ""
                getNextChar()
                return
            else:
                token = "ID"
        
        getNextChar()

    f_out.write(token + '\t' + lexeme + '\n')

    # reset lexeme for next token/lexeme pair
    lexeme = ""


def handleCharConstant():
    global ch
    global lexeme
    global token
    global tokenCount
    global f_out

    token = "CHAR_CONST"
    option1 = False
    op2Count = 1
    getNextChar()

    # Loop until character isn't recognized as a char const format
    #   add to current lexeme if it is recognized
    while ch != '\'':
        lexeme += ch
        option1 = True
        getNextChar()

    # Checking if its '''' instead of 'INSERT HERE'
    if option1 is False:
        while ch == '\'':
            getNextChar()
            op2Count += 1

        if op2Count != 4:
            f_out.write("SYNTAX ERROR: Check your const_identifier!")
        else:
            f_out.write(token + '\n')
    else:
        f_out.write(token + '\t' + lexeme + '\n')

    getNextChar()
    lexeme = ""


def handleIntegerConstant():
    global ch
    global token
    global lexeme
    global tokenCount
    global f_out

    token = "INT_CONST"
    lexeme += ch
    getNextChar()

    # Loop until ch isn't recognized as a number.
    #   Add to current lexeme if it is recognized.
    while ch in miniPascalDigits:
        lexeme += ch
        getNextChar()

    f_out.write(token + '\t' + lexeme + '\n')
    tokenCount += 1
    lexeme = ""


def handleOtherTokens():
    global ch
    global token
    global f_out
    global tokenCount

    token = miniPascalOtherTokens[ch]
    f_out.write(token + '\n')
#    tokenCount += 1 TODO
    getNextChar()


if __name__ == "__main__":
    main()


# When encountered with error, could output error that you know of
#   And then ignore everything until the semicolon. (Possible another way)
