# -------------------------------------------------------------------------- #
#   By Robert Chung                                                          #
#   HW for CSC 3310 - Concepts in Programming Languages                      #
#   Dr. Arias                                                                #
#   lexer2.py                                                                #
#   This program should take a program written in Mini-Pascal and output     #
#   the Tokens and Lexemes into a new file.                                  #
# ------------------------  EXTRA CREDIT ----------------------------------- #

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
                         '>': "GRTHAN", "<=": "LTOREQ", ">=": "GTOREQ",
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
miniPascalIdentifiers = {
                         "integer", "Boolean", "True", "False"
                        }

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

    # ----------------------------------------------------------------------- #
    #                      ======= FILE OPENING =======                       #
    #                           Opening Input File                            #
    try:
        inputFile = sys.argv[1]
    except:
        print "ERROR: Did you specify a file to print to?"
        return
    try:
        f = open(inputFile, 'r')
    except IOError:
        print "ERROR: Unable to open the file you specified! Please try again."
        return
    # ----------------------------------------------------------------------- #
    #                     Opening Output File for writing
    outputFile = inputFile.split('.')[0] + ".out"
    try:
        f_out = open(outputFile, 'w')
    except IOError:
        print "ERROR: Error creating new file for writing"
        return
    # ======================================================================= #

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
        f_out.write("LEXICAL ERROR: Character not recognized!\n")
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
        getNextChar()

    if lexeme in miniPascalOtherTokens:
        token = miniPascalOtherTokens[lexeme]
        f_out.write(token + '\n')
    elif lexeme in miniPascalIdentifiers:
        token = "PREDEFINED ID"
        f_out.write(token + '\t' + lexeme + '\n')
    else:
        f_out.write(token + '\t' + lexeme + '\n')

    tokenCount += 1
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
            f_out.write("LEXICAL ERROR: Check your const_identifier!\n")
            return
        else:
            f_out.write(token + '\n')
    else:
        f_out.write(token + '\t' + lexeme + '\n')

    tokenCount += 1

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


# changed where to do getChar()
def handleOtherTokens():
    global ch
    global token
    global f_out
    global tokenCount

    possibleToken = ch
    tempCh = ch

    # Taking care of multi-character tokens
    if ch == '.' or ch == '>' or ch == '<' or ch == ':':
        getNextChar()
        possibleToken += ch
        if possibleToken in miniPascalOtherTokens:
            token = miniPascalOtherTokens[possibleToken]
            f_out.write(token + '\n')
            getNextChar()
        else:
            token = miniPascalOtherTokens[tempCh]
            f_out.write(token + '\n')
    else:
        token = miniPascalOtherTokens[ch]
        f_out.write(token + '\n')
        getNextChar()

    tokenCount += 1


if __name__ == "__main__":
    main()
