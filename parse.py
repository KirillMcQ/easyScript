#!/usr/bin/env python3


'''
Boring classes which caused me to make this
  - Biology
  - ELA
  - Healthcare
  - Civics
  - Math

Important NOTE about function calling and declaring in this language:
  Function parameters are separated by a '|'. For example: someFunc(param1|param2|param3)
'''
# Get checker functions from helpers dir
from helpers.checkers import *
# For getting command line argument of file name
import sys

# Make sure the user has supplied the correct amount of arguments from the command line
n = len(sys.argv)
if n < 2 or n > 2:
    err('exec', 0, 'invalid execution command! usage: python3 parse.py {fileName.myLang}')

# Open the file in read mode. Hardcoded name for now.
inputtedFile = sys.argv[1] # The filename
file = open(inputtedFile, "r")
# Global Vars
lineNo = 1
userVars = {} # Holds the variables the user creates
builtInFuncs = ["print", "readIn"] # Hold all of the built-in functions
isInIf = False # Will hold if the program is currently inside of an if statement
isIfExprTrue = False # Will hold if the if statement expression is true or false
curIfStatementCode = [] # Will hold the code of the current if statement

# Iterate through program lines
for line in file:
    # Remove new line from the current line
    line = line.replace("\n", "")
    # Skip this line if it is a comment
    if isComment(line):
        lineNo+=1
        continue
    # Exit program with error if lines doesn't end with semi-colon
    # If statement declarations and endif declarations are exempt
    if not endsWithSemiColon(line) and not isIfStatement(line) and not isEndingIf(line) and line:
        err('syntax', lineNo, 'line must end with semi-colon!')
    # Check if the current line is an ENDIF
    if isEndingIf(line):
        if isIfStatement:
            # Reset all of the variables not needed for code execution
            isInIf = False
            ifExpr = False
            isIfExprTrue = False
            # Execute the code
            for code in curIfStatementCode:
                # Check if it is a variable assignment by calling the helper function
                # Remove leading and trailing whitespace
                code = code.strip()
                if isVariableDecleration(code):
                    userVars = handleVarDec(code, userVars, lineNo, builtInFuncs)
                if isFuncCall(code):
                    handleFuncCall(code, builtInFuncs, lineNo, userVars)
            # Reset the curCode arr
            curIfStatementCode = []
        if not isIfStatement:
            err('keyword', lineNo, 'you can only use ENDIF if you are currently in an if statement!')
    # Check if we are currently inside of an if statement
    if isIfStatement:
        # Append to the current if statement code if the expression was True
        if isIfExprTrue:
            curIfStatementCode.append(line)
    
    # Check if it is a variable assignment by calling the helper function
    if isVariableDecleration(line):
        userVars = handleVarDec(line, userVars, lineNo, builtInFuncs)
    # Check if it is a function call
    if isFuncCall(line):
        handleFuncCall(line, builtInFuncs, lineNo, userVars)
    if isIfStatement(line):
        isInIf = True
        finalExpr = getFinalExpr(line, lineNo, userVars)
        isIfExprTrue = eval(finalExpr)

    lineNo+=1