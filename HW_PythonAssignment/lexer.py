# -------------------------------------------------------------------------- #
#   By Robert Chung                                                          #
#   HW for CSC 3310 - Concepts in Programming Languages                      #
#   Dr. Arias                                                                #
#   lexer.py                                                                #
#   This program should take a program written in Mini-Power and output      #
#   the Tokens and Lexemes into a new file.                                  #
# -------------------------------------------------------------------------- #

import sys

miniPowerLetters = (
                    'a', 'b', 'c', 'd', 'e', 'f', 'e', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x', 'y', 'z'
                    )
miniPowerDigits = (
                   '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
                  )
miniPowerOtherTokens = {
                        ';': "SEMICOLON", '+': "PLUS", '-': "MINUS",
                        '*': "TIMES", '/': "DIV", '^': "POWER", '=': "ASSIGN",
                        '\"': "STRING", '(': "LPAREN", ')': "RPAREN"
                       }
miniPowerType = {
                 '#': "INTEGER", '%': "REAL", '$': "STRING"
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


# getNextChar gets next character in file
def getNextChar():
    global ch
    global f

    # process the next character if its not EOF
    if ch != "":
        ch = f.read(1)


# getNextNonWhiteSpace gets next non white space character in file
def getNextNonWhiteSpace():
    global ch
    global f

    while ch == " " or ch == '\n' or ch == '\t':
        getNextChar()


# lex gets the next token and lexeme
def lex():
    global ch
    global f_out

    getNextNonWhiteSpace()
    if ch in miniPowerLetters:
        handleIDToken()
    elif ch == '\"':
        handleSTRINGToken()
    elif ch in miniPowerOtherTokens:
        handleOtherTokens()
    elif ch in miniPowerDigits:
        handleNumbers()
    elif ch == 'P':
        checkAndHandlePrintToken()
    elif ch == "":
        return
    else:
        f_out.write("LEXICAL ERROR: Character not recognized!\n")
        getNextChar()


# handleIDToken handles figuring out ID tokens
def handleIDToken():
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
    while ch in miniPowerLetters or ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    # ID must end with a type symbol.
    #   If not, then it should be error.
    if ch in miniPowerType:
        f_out.write(token + '\t' + lexeme + '\t' + miniPowerType[ch] + '\n')
        tokenCount += 1
    else:
        f_out.write("LEXICAL ERROR: Didn't find ID Type!"
                    " Check your whitespace or ID syntax!\n")

    getNextChar()
    # reset lexeme for next token/lexeme pair
    lexeme = ""


# handleSTRINGToken handles figuring out string tokens
def handleSTRINGToken():
    global ch
    global lexeme
    global token
    global tokenCount
    global f_out

    # Quotation is a token.
    token = "QUOTE"
    f_out.write(token + '\n')
    tokenCount += 1

    # Now doing String
    token = "STRING"
    getNextChar()

    # Loop until character isn't recognized as a string format
    #   add to current lexeme if it is recognized
    while ch in miniPowerLetters or ch in miniPowerDigits or ch == ' ':
        lexeme += ch
        getNextChar()

    # String must end with a ".
    #   If not, then it should be an error.
    if ch == '\"':
        f_out.write(token + '\t' + lexeme + '\n')
        f_out.write("QUOTE" + '\n')
        tokenCount += 2
    else:
        f_out.write("LEXICAL ERROR: Incorrect String Format. "
                    "Are you missing a \"? \n")

    getNextChar()
    lexeme = ""


# handleNumbers handles numbers that it comes across and checks to see
#   if it is a REAL_CONST or INT_CONST
def handleNumbers():
    global ch
    global token
    global lexeme
    global tokenCount
    global f_out

    # Before encountering a '.' all we know is that it's a INT_CONST.
    #   We will later check and update if we encounter a '.'
    token = "INT_CONST"
    lexeme += ch
    getNextChar()

    # Loop until ch isn't recognized as a number.
    #   Add to current lexeme if it is recognized.
    while ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    # Check to see if the number was a decimal number
    #   Update the token to a real const if it is.
    if ch == '.':
        token = "REAL_CONST"
        lexeme += ch
        getNextChar()

        # Same loop as above, just getting rest of the numbers.
        while ch in miniPowerDigits:
            lexeme += ch
            getNextChar()

    f_out.write(token + '\t' + lexeme + '\n')
    tokenCount += 1
    lexeme = ""


# checkAndHandlePrintToken handles the PRINT token
def checkAndHandlePrintToken():
    global ch
    global token
    global lexeme
    global f_out
    global tokenCount

    # Not really that efficient imo, TODO make it better
    printStr = "PRINT"
    stringComp = ""
    while ch in printStr:
        stringComp += ch
        getNextChar()

    if stringComp == printStr:
        token = "PRINT"
        f_out.write(token + '\n')
        tokenCount += 1
    else:
        f_out.write("LEXICAL ERROR: Did you mean PRINT?\n")

    getNextChar()


# handleOtherTokens takes care of any other tokens that are valid
def handleOtherTokens():
    global ch
    global token
    global f_out
    global tokenCount

    token = miniPowerOtherTokens[ch]
    f_out.write(token + '\n')
    tokenCount += 1
    getNextChar()


if __name__ == "__main__":
    main()
