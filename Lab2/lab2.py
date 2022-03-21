import sys

predicates = []
variables = []
constants = []
functions = []
clauses = []


def extractVariable(c):
    return c[c.find('(') + 1:c.rfind(')')]


def parseVariables(ci, cj):
    ciVariable = extractVariable(ci)
    cjVariable = extractVariable(cj)
    ciVariablesSplit = ciVariable.split(",")
    cjVariablesSplit = cjVariable.split(",")
    return ciVariable, cjVariable, ciVariablesSplit, cjVariablesSplit


def bracketsCountFor(clause):
    brackets = 0
    for b in clause:
        if b == "(" or b == ")":
            brackets = brackets + 1
    return brackets


def fourBracketsForBoth(c1, c2):
    if c1.split("(")[0] in functions:
        ciVariable = extractVariable(c1)
        cjVariable = extractVariable(c2)
        if ciVariable in variables:
            c1 = c1.replace(ciVariable, cjVariable)
        elif cjVariable in variables:
            c2 = c2.replace(cjVariable, ciVariable)
    return c1, c2


def fourOrTwoBrackets(c, ci, cj):
    if c.split("(")[0] in functions:
        cjVariable = extractVariable(cj)
        if cjVariable in variables:
            cj = cj.replace(cjVariable, c)
    return ci, cj


def twoOrFourBrackets(c, ci, cj):
    if c.split("(")[0] in functions:
        ciVariable = extractVariable(ci)
        if ciVariable in variables:
            ci = ci.replace(ciVariable, c)
    return ci, cj


def twoBracketsForBoth(c1, ci, c2, cj):
    if c1 in variables:
        ci = ci.replace(c1, c2)
    elif c2 in variables:
        cj = cj.replace(c2, c1)
    return ci, cj


def parseDataForFunctions(ci, cj):
    _, _, ciVariableSet, cjVariableSet = parseVariables(ci, cj)

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:
        for i in range(len(ciVariableSet)):
            if ciVariableSet[i].find("(") != -1:
                ciItemInVariable = ciVariableSet[i]
                cjItemInVariable = cjVariableSet[i]
                ci, cj = fourBracketsForBoth(ciItemInVariable, cjItemInVariable)
                return ci, cj

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) != 4:
        for i in range(len(cjVariableSet)):
            if cjVariableSet[i] in variables:
                cj = cj.replace(cjVariableSet[i], ciVariableSet[i])
        return ci, cj

    if bracketsCountFor(ci) != 4 and bracketsCountFor(cj) == 4:
        for i in range(len(ciVariableSet)):
            if ciVariableSet[i] in variables:
                ci = ci.replace(ciVariableSet[i], cjVariableSet[i])
        return ci, cj
    return ci, cj


def unification(ci, cj):
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

    elif ci.find(",") != -1:
        return ci, cj

    elif cj.find(",") != -1:
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
    returns all clauses that can be obtained from clauses ci and cj
    """
    resolvents = []
    ciOriginal = ci.split(" ")
    cjOriginal = cj.split(" ")
    for i in ciOriginal:
        for j in cjOriginal:
            iUnified, jUnified = unification(i, j)  # Unify two to see if it can be same
            if iUnified == ("!" + jUnified) or ("!" + iUnified) == jUnified:  #
                ciTemp = ci.split(" ")
                ciTemp.remove(i)
                cjTemp = cj.split(" ")
                cjTemp.remove(j)
                resolvents = clausesAfterResolution(ciTemp, cjTemp)
    return resolvents


def plResolution(kb):  # resolution function return true or false
    # print(Clauses_set)
    newList = []
    while True:
        allPairs = [(kb[i], kb[j]) for i in range(len(kb)) for j in
                    range(i + 1, len(kb))]  # make pair from all possible Clauses
        for (ci, cj) in allPairs:
            resolvents = plResolve(ci, cj)  # Call Resolver
            # print(resolvents)
            if [] in resolvents:  # if the empty Clauses we return T
                return True
            for temp in resolvents:
                if temp not in newList:
                    newList.append(temp)

        if set(newList).issubset(kb):
            return False

        for clause in newList:
            if clause not in kb:
                kb.append(clause)


def checkData():
    if plResolution(clauses):
        print("no")
    else:
        print("yes")


if len(sys.argv) < 1:
    print("Invalid number of arguments!")
    sys.exit(1)
else:
    with open("/Users/abhishekshah/Documents/Spring 22/Ass-AI-630/AI Lab2/testcases/prop/p02.cnf") as f:
        lines = f.readlines()
        predicates = lines[0].split()[1:]
        variables = lines[1].split()[1:]
        constants = lines[2].split()[1:]
        functions = lines[3].split()[1:]
        for i in range(5, len(lines)):
            clauses.append(lines[i].strip().rstrip('\n'))


if __name__ == "__main__":
    checkData()
