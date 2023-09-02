'''
This file is created for use in ../parse.py
The functions are used mainly for checking a line of code and detecting what is happening
NOTE: All lines except comments MUST end with a semicolon(';')
'''
# For RegEx Matching
import re

'''
Check if line of code is a comment
Comment is denoted by '//'
returns: True if line is comment
returns: False if line is not comment
'''
def isComment(line):
    return line.startswith('//')

'''
Check if line ends with semi-colon
returns: True if line ends with semi-colon
returns: False if line does not end with a semi-colon
'''
def endsWithSemiColon(line):
    return line.endswith(';')

'''
Show an error. Will exit the program after printing the issue
returns: nothing, because the program is exited
Accepts the error type (like 'syntax', 'type')
Accepts the line number
Accepts the error message
'''
def err(errType, lineNo, msg):
    print(errType + ' error on line ' + str(lineNo) + ': ' + msg)
    exit()

'''
Check if line a variable decleration/assignment
Variable decleration is defined like this: 'VARIABLE b = 2;'
returns: True if line is a variable decleration
returns: False if line is not a variable decleration
'''
def isVariableDecleration(line):
    # If the line doesn't begin with 'VARIABLE', it isn't a valid variable decleration
    if not line.startswith('VARIABLE'):
        return False
    # If there is no '=', it isn't a valid variable decleration
    if not '=' in line:
        return False

    return True

'''
This function will return a stripped down variable decleration for storing the var value in ../main.py
Assumes that the line is a valid variable decleration
returns: 'varName=value', which makes it easy to assign the variable in the main file.
'''
def evalVariableDecleration(line):
    # Remove the 'VARIABLE' keyword from the line, remove spaces, remove semi-colon
    # return line.replace('VARIABLE', '').replace(' ', '').replace(';', '')
    return line.replace('VARIABLE', '').replace(';', '')

'''
This function will determine if a given value is a float or not
returns: True if param is a float
returns: False if param is not a float
'''
def isFloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

'''
This function will determine if a given value is a boolean or not
returns: True if it is a boolean
returns: False if it is not a boolean
'''
def isBool(val):
    return val == 'True' or val == 'False'

'''
This function will determine if a given line is a function invokation (a function call)
Read the note in ../main.py to understand separating parameters and arguments in the language
Example: isFuncCall('print()') -> True
Example: isFuncCall('defNotAFuncCall') -> False
Example: isFuncCall('aFunc("Param1"|"Param2")') -> True
'''
def isFuncCall(line):
    # Check if the line matches the function pattern regex
    result = re.search("[a-zA-Z]+\([a-zA-Z0-9\,\'\"\s!\|:]*\)", line)
    if result:
        return True

'''
This function will handle a function call
Accepts: The line (the function call)
Accepts: The builtInFuncs array (contains all of the built-in language functions)
Accepts: The line number (lineNo)
Accepts: The user variable obj varObj
returns: a function return value if it has one
returns: None if there is no return value
'''
def handleFuncCall(line, builtInFuncs, lineNo, varObj):
      # Assume no return value until otherwise discovered
      returnVal = None
      # Remove Semi-colon
      line = line.replace(';', '')
      # Split the function call into seperate parts
      line = line.split("(");
      # Get the funcName and params
      funcName = line[0]
      params = line[1][:-1] # gets the second el of line and also removes the closing paren
      # Look at the comment at the start of the ../parse.py file about separating params
      params = params.split('|')
      # Remove the quotes from the parameters if they are string
      # Also,
      '''
      Check if any of the parameters are variable names, and if so, replace the value with the variable value
      '''
      for i in range(len(params)):
          if isinstance(params[i], str):
              params[i] = params[i].replace("'", '').replace('"', "")
          if params[i] in varObj:
              params[i] = handleVarVal(params[i], varObj)
      

      # Check if the function name is in the built-in functions
      if funcName in builtInFuncs:
          '''
          Harcode the function names for now, because there are only 2 built-in funcs at the time of writing
          '''
          if funcName == 'print':
              # Print what the user provided, and spread the parameters out in the func call
              print(*params)
          elif funcName == 'readIn':
              # 'readIn' is the equivalent to 'input' in python
              returnVal = input(*params)
      return returnVal

'''
This function will determine a given variable's value
Accepts: the variable name
Accepts: the varObj object (contains varName:value)
Returns: the variable value
'''
def handleVarVal(varName, varObj):
    return varObj[varName]

'''
This function will determine if a given line is an if statement
if statement syntax:

(1 > 3) ? STARTIF
    print("Do something here")
ENDIF

Accepts: the current line
returns: True if the line is an if statement
returns: False if the line is not an if statement
'''
def isIfStatement(line):
    result = re.search("\([^)]+\)\s+\?\s+STARTIF", line)
    if result:
        return True
    return False

'''
This function will determine if the given line is the ending to an if statement
Accepts: the current line
returns: True if the line is equal to 'ENDIF'
returns: False if the line is not equal to 'ENDIF'
'''
def isEndingIf(line):
    return line == "ENDIF"

'''
This function will return a string that is the if statement expression.
if statement syntax:

(1 > 3) ? STARTIF

Accepts: the if statement decleration line
returns: string of the expression
'''
def getIfExpr(ifStatement):
    # Replace everything except for the expression
    expression = ifStatement.replace(' ', '').replace('STARTIF', '').replace('?', '')
    return expression

'''
This function will replace all of the varnames inside of an if expression with their respective values
Accepts: the current if statement expression arguments as an array
Accepts: the line number
Accepts: the current varObj object which contains the varname:varvalue pairs
returns: an array with the correct values with replaced varnames for varvals
'''
def replaceIfExprVars(exprArr, lineNo, varObj):
    outArr = []
    for arg in exprArr:
        if arg in varObj:
            outArr.append(handleVarVal(arg, varObj))
        else:
            # Just make sure the value of the argument is correct, and then append to the output array
            outArr.append(detectConvertVal(arg))
    return outArr

'''
This function will handle a variable decleration, by assigning a varname to a varval
Accepts: the current line
Accepts: the varObj to assign the variable to
Accepts: the current line number
Accepts: the builtInFuncs obj
returns: the updated varObj
'''
def handleVarDec(line, varObj, lineNo, builtInFuncs):
        simplifiedVarExpr = evalVariableDecleration(line)
        simplifiedVarExpr = simplifiedVarExpr.split('=')
        assignedVal = simplifiedVarExpr[1].strip() # Value
        assignedName = simplifiedVarExpr[0].strip() # Name
        # Check the type of the variable
        if assignedVal.isdigit():
            varObj[assignedName] = int(assignedVal)
        elif isFloat(assignedVal):
            varObj[assignedName] = float(assignedVal)
        elif isBool(assignedVal):
            varObj[assignedName] = bool(assignedVal)
        else:
            '''
            Check for a string (if it contains single or double quotes) and make sure it isn't a func call
            '''
            if "'" in assignedVal or '"' in assignedVal and not isFuncCall(assignedVal):
                # A string
                varObj[assignedName] = assignedVal.replace("'", '').replace('"', '')
            elif assignedVal in varObj:
                # No quotes, only option is it is another variable
                varObj[assignedName] = varObj[assignedVal]
            elif isFuncCall(assignedVal):
                '''
                NOTE: The readIn function with automatically determine the inputted type. No need for the user to do that.
                '''
                # A function call is the assigned variable value
                # If the called function has no return value, the value with be 'None'
                assignedVal = assignedVal.strip()
                assignedName = assignedName.strip()
                funcReturn = handleFuncCall(assignedVal, builtInFuncs, lineNo, varObj)
                # Check the return type
                varObj[assignedName] = detectConvertVal(funcReturn)
            else:
                # Not a string or a created variable
                err('syntax', lineNo, 'symbol ' + assignedVal + ' not found')
        return varObj

'''
This function will detect the data type of the inputted val, and return the converted value
Accepts: the input value
returns: the converted value
'''
def detectConvertVal(val):
    if val.isdigit():
        val = int(val)
    elif isFloat(val):
        val = float(val)
    elif isBool(val):
        val = bool(val)
    return val

'''
This function will return the operator of an if expression
Accepts: the expression
returns: the operator as a string
'''
def getIfOp(expr):
    op = ""
    for i in expr:
        if not i.isdigit() and not i.isalpha() and i != "(" and i != ")":
            op+=i
        elif op:
            return op

'''
This function will get the final if expression to be evaluated with eval()
Accepts: the current line
Accepts: the line number
Accepts: the varObj objects that contains user created variables and their respective values
returns: an updated expression
'''
def getFinalExpr(line, lineNo, varObj):
    ifExpr = getIfExpr(line)
    ifExprSplit = re.split("[\W_]+", ifExpr)
    # Get the operator using regex
    getOp = getIfOp(ifExpr)
    ifExprSplit = [part for part in ifExprSplit if part] # Filter out the empty strings
    updatedExpr = replaceIfExprVars(ifExprSplit, lineNo, varObj) # Get an array returned with the replaced values
    finalExpr = str(updatedExpr[0]) + getOp + str(updatedExpr[1])
    return finalExpr