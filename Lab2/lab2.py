"""
file: lab2.py
description: CSCI 630, Lab 2, Resolution
language: Python
author: Abhishek Shah, as5553
"""
import sys


def extractVariable(c):
    """
    Logic for extracting variables given any function with brackets
    """
    return c[c.find('(') + 1:c.rfind(')')]


def parseVariables(ci, cj):
    """
    Logic for reading variables from functions
    """
    ciVariable = extractVariable(ci)
    cjVariable = extractVariable(cj)
    ciVariablesSplit = ciVariable.split(",")
    cjVariablesSplit = cjVariable.split(",")
    return ciVariable, cjVariable, ciVariablesSplit, cjVariablesSplit


def fourBracketsForBoth(ci, cj):
    """
    Logic for when ci and cj have 4 brackets in total
    """
    if ci.split("(")[0] in functions:
        ciVariable = extractVariable(ci)
        cjVariable = extractVariable(cj)
        if ciVariable in variables:
            ci = ci.replace(ciVariable, cjVariable)
        elif cjVariable in variables:
            cj = cj.replace(cjVariable, ciVariable)
    return ci, cj


def fourOrTwoBrackets(c, ci, cj):
    """
    Logic for when ci has 4 brackets and cj has 2 brackets
    """
    if c.split("(")[0] in functions:
        cjVariable = extractVariable(cj)
        if cjVariable in variables:
            cj = cj.replace(cjVariable, c)
    return ci, cj


def twoOrFourBrackets(c, ci, cj):
    """
    Logic for when ci has 2 brackets and cj has 4 brackets
    """
    if c.split("(")[0] in functions:
        ciVariable = extractVariable(ci)
        if ciVariable in variables:
            ci = ci.replace(ciVariable, c)
    return ci, cj


def twoBracketsForBoth(c1, ci, c2, cj):
    """
    Logic for when ci and cj have 2 brackets in total
    """
    if c1 in variables:
        ci = ci.replace(c1, c2)
    elif c2 in variables:
        cj = cj.replace(c2, c1)
    return ci, cj


def bracketsCountFor(clause):
    """
    Logic for counting total brackets in a clause
    """
    brackets = 0
    for b in clause:
        if b == "(" or b == ")":
            brackets = brackets + 1
    return brackets


def parseDataForFunctions(ci, cj):
    """
    Parsing data for files which contains functions, especially the SK() functions.
    """
    _, _, ciVariableSet, cjVariableSet = parseVariables(ci, cj)

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:
        for item in range(len(ciVariableSet)):
            if ciVariableSet[item].find("(") != -1:
                ciItemInVariable = ciVariableSet[item]
                cjItemInVariable = cjVariableSet[item]
                ci, cj = fourBracketsForBoth(ciItemInVariable, cjItemInVariable)
                return ci, cj

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) != 4:
        for item in range(len(cjVariableSet)):
            if cjVariableSet[item] in variables:
                cj = cj.replace(cjVariableSet[item], ciVariableSet[item])
        return ci, cj

    if bracketsCountFor(ci) != 4 and bracketsCountFor(cj) == 4:
        for item in range(len(ciVariableSet)):
            if ciVariableSet[item] in variables:
                ci = ci.replace(ciVariableSet[item], cjVariableSet[item])
        return ci, cj
    return ci, cj


def unification(ci, cj):
    """
    Unifying two clauses to see if they can be same or not
    """
    ciVariable = extractVariable(ci)
    cjVariable = extractVariable(cj)
    if ci.find(",") != -1 and cj.find(",") != -1:
        if bracketsCountFor(ci) == 4 or bracketsCountFor(cj) == 4:
            ci, cj = parseDataForFunctions(ci, cj)
        ciVariable, cjVariable, ciVariableSet, cjVariableSet = parseVariables(ci, cj)
        temp = []

        for item in range(len(ciVariableSet)):
            if ciVariableSet[item] in variables:
                ci = ci.replace(ciVariableSet[item], cjVariableSet[item])
                temp.append(cjVariableSet[item])
        for item in temp:
            cjVariableSet.remove(item)

        for item in range(len(cjVariableSet)):
            if cjVariableSet[item] in variables:
                cj = cj.replace(cjVariableSet[item], ciVariableSet[item])
        return ci, cj
    else:
        if bracketsCountFor(ci) == 2 and bracketsCountFor(cj) == 2:  # only one variable or const
            ci, cj = twoBracketsForBoth(ciVariable, ci, cjVariable, cj)
            return ci, cj
        else:
            if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:
                ci, cj = fourBracketsForBoth(ciVariable, cjVariable)
                return ci, cj

            elif bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 2:
                ci, cj = fourOrTwoBrackets(ciVariable, ci, cj)
                return ci, cj
            else:
                ci, cj = twoOrFourBrackets(cjVariable, ci, cj)
                return ci, cj


def clausesAfterResolution(ci, cj):
    """
    returns clauses in proper str " " format after resolving and removing them
    """
    clausesPostResolution = []
    ciNew = ""
    if len(ci) > 1:
        spaceBetweenClauses = " "
    else:
        spaceBetweenClauses = ""

    for item in ci:
        if ciNew != "":
            ciNew = ciNew + spaceBetweenClauses + item
        else:
            ciNew = ciNew + item

    cjNew = ""
    if len(cj) > 1:
        spaceBetweenClauses = " "
    else:
        spaceBetweenClauses = ""

    for item in cj:
        if cjNew != "":
            cjNew = cjNew + spaceBetweenClauses + item
        else:
            cjNew = cjNew + item

    if ciNew == "" and cjNew == "":
        clausesPostResolution.append([])

    if cjNew == "" or ciNew == "":
        clausesPostResolution.append(ciNew + cjNew)
    else:
        clausesPostResolution.append(ciNew + " " + cjNew)
    return clausesPostResolution


def plResolve(ci, cj):  # return all possibility from two Clauses
    """
    returns clauses that can be obtained after resolving clauses ci and cj
    """
    resolvents = []
    ciOriginal = ci.split(" ")
    cjOriginal = cj.split(" ")
    for i in ciOriginal:
        for j in cjOriginal:
            iUnified, jUnified = unification(i, j)
            if iUnified == ("!" + jUnified) or ("!" + iUnified) == jUnified:
                ciTemp = ci.split(" ")
                cjTemp = cj.split(" ")
                ciTemp.remove(i)
                cjTemp.remove(j)
                resolvents = clausesAfterResolution(ciTemp, cjTemp)
    return resolvents


def plResolution(kb):  # resolution function return true or false
    """
    returns true or false
    """
    newList = []
    while True:
        allPairs = [(kb[i], kb[j]) for i in range(len(kb)) for j in
                    range(i + 1, len(kb))]
        for (ci, cj) in allPairs:
            resolvents = plResolve(ci, cj)
            # if resolvents have empty clause
            if [] in resolvents:
                return True
            for temp in resolvents:
                if temp not in newList: newList.append(temp)
        if set(newList).issubset(kb):
            return False
        for clause in newList:
            if clause not in kb:
                kb.append(clause)


def checkData():
    if plResolution(clauses): print("no")
    else: print("yes")


predicates = []
variables = []
constants = []
functions = []
clauses = []


if len(sys.argv) < 1:
    print("Invalid number of arguments!")
    sys.exit(1)
else:
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        predicates = lines[0].split()[1:]
        variables = lines[1].split()[1:]
        constants = lines[2].split()[1:]
        functions = lines[3].split()[1:]
        for i in range(5, len(lines)):
            clauses.append(lines[i].strip().rstrip('\n'))


def main():
    checkData()


if __name__ == "__main__":
    main()
