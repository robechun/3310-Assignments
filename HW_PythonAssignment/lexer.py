# By Robert Chung
# HW for CSC 3310 - Concepts in Programming Languages
# Dr. Arias
# Lexer.py
# This program should take a program written in Mini-Power and output the
#   Tokens and Lexemes into a new file.


# QUESTIONS TO ASK
# 1) Are we assuming the syntax is correct? or do we not care
# 2) Are we assuming grammer is correct? or do we not care
# 3) Are there restrictions on libraries that we can import?
# 4) is it INT_CONST or INTEGER? (same with REAL_CONST)

# QUESTIONS:
# 1) Do we exit from program if we find a syntax error? Or do we keep going?
# 2) The last semicolon
# 3) Example has different names for INTEGER->INT and PLUS->ADD
# 4) Formatting the output (spaces and stuff)
# 5) String token?? the : after a string

# TODO
# 1) The last semicolon
# 2) Put it into an actual file instead of just printing
# 3) Check program with tests (Faults)
# 4) Extra credit?

import sys

miniPowerLetters = ('a', 'b', 'c', 'd', 'e', 'f', 'e', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x', 'y', 'z')
miniPowerDigits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
miniPowerOtherTokens = {';': "SEMICOLON", '+': "PLUS", '-': "MINUS",
                        '*': "TIMES", '/': "DIV", '^': "POWER", '=': "ASSIGN",
                        '\"': "STRING", '(': "LPAREN", ')': "RPAREN"}
miniPowerType = {'#': "INTEGER", '%': "REAL", '$': "STRING"}


f = ""

ch = " "
token = ""
lexeme = ""


def main():
    global f

    # Opening Input File
    inputFile = sys.argv[1]
    try:
        f = open(inputFile, 'r')
    except IOError:
        print "Unable to open the file you specificed! Please try again."
        return
   
    while ch != "":
        lex()


def getNextChar():
    global ch
    global f

    # process the next character if its not EOF
    if ch != "":
        ch = f.read(1)


def getNextNonWhiteSpace():
    global ch
    global f

    while ch == " " or ch == '\n':
        getNextChar()


def lex():
    global ch

    getNextNonWhiteSpace()
    if ch in miniPowerLetters:
        handleIDToken()
    elif ch == '\"':
        handleSTRINGToken()
    elif ch in miniPowerOtherTokens:
        token = miniPowerOtherTokens[ch]
        print token
        getNextChar()
    elif ch in miniPowerDigits:
        handleNumbers()
    elif ch == 'P':
        checkAndHandlePrintToken()
    

def handleIDToken():
    global ch
    global token
    global lexeme

    token = "ID"
    lexeme += ch
    getNextChar()
    while ch in miniPowerLetters or ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    if ch in miniPowerType:
        print token, "  ", lexeme, "  ", miniPowerType[ch]
    else:
        print "ERROR WRONG ID"
    lexeme = ""
    getNextChar()


def handleSTRINGToken():
    global ch
    global lexeme
    global token

    token = "STRING"
    getNextChar()
    while ch in miniPowerLetters or ch in miniPowerDigits or ch == ' ':
        lexeme += ch
        getNextChar()
    if ch != '\"':
        print "ERROR WRONG STRING FORMAT"
    else:
        print token, "       ", lexeme
    lexeme = ""
    getNextChar()


def handleNumbers():
    global ch
    global token
    global lexeme

    token = "INT_CONST"
    lexeme += ch
    getNextChar()
    while ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    if ch == '.':
        token = "REAL_CONST"
        lexeme += ch
        getNextChar()
        while ch in miniPowerDigits:
            lexeme += ch
            getNextChar()
    print token, "  ", lexeme

    lexeme = ""


# TODO TEST with faulty print
def checkAndHandlePrintToken():
    global ch
    global token
    global lexeme

    printStr = "PRINT"
    stringComp = ""
    while ch in printStr:
        stringComp += ch
        getNextChar()

    if stringComp != printStr:
        print "INVALID STRING THING, DID YOU MEAN PRINT?"
    else:
        token = "PRINT"
        print token
        getNextChar()


if __name__ == "__main__":
    main()
