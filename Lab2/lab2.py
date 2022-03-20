import sys

Predicates = []
Variables = []
Constants = []
Functions = []
Clauses = []


def bracketsCountFor(clause):
    brackets = 0
    for b in clause:
        if b == "(" or b == ")":
            brackets = brackets + 1
    return brackets


def parseVariables(ci, cj):
    ciVariable = ci[ci.find('(') + 1:ci.rfind(')')]
    cjVariable = cj[cj.find('(') + 1:cj.rfind(')')]
    ciVariablesSplit = ciVariable.split(",")
    cjVariablesSplit = cjVariable.split(",")
    return ciVariable, cjVariable, ciVariablesSplit, cjVariablesSplit


def parseDataForFunctions(ci, cj):

    _, _, ciVariableSet, cjVariableSet = parseVariables(ci, cj)

    if bracketsCountFor(ci) != 4 and bracketsCountFor(cj) == 4:
        for i in range(len(ciVariableSet)):
            if ciVariableSet[i] in Variables:
                ci = ci.replace(ciVariableSet[i], cjVariableSet[i])
        return ci, cj

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) != 4:
        for i in range(len(cjVariableSet)):
            if cjVariableSet[i] in Variables:
                cj = cj.replace(cjVariableSet[i], ciVariableSet[i])
        return ci, cj

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:
        for i in range(len(ciVariableSet)):
            if ciVariableSet[i].find("(") != -1:
                ciItemInVariable = ciVariableSet[i]
                cjItemInVariable = cjVariableSet[i]
                if ciItemInVariable.split("(")[0] in Functions:
                    ciVariable = ciItemInVariable[ciItemInVariable.find('(') + 1:ciItemInVariable.rfind(')')]
                    cjVariable = cjItemInVariable[cjItemInVariable.find('(') + 1:cjItemInVariable.rfind(')')]
                    if ciVariable in Variables:
                        ci = ci.replace(ciVariable, cjVariable)
                    elif cjVariable in Variables:
                        cj = cj.replace(cjVariable, ciVariable)
                return ci, cj

    return ci, cj


def unify(ci, cj):
    if ci.find(",") != -1 and cj.find(",") != -1:
        if bracketsCountFor(ci) == 4 or bracketsCountFor(cj) == 4:
            ci, cj = parseDataForFunctions(ci, cj)

        ciVariable, cjVariable, ciVariableSet, cjVariableSet = parseVariables(ci, cj)

        remove_spot = []
        for i in range(len(ciVariableSet)):
            if ciVariableSet[i] in Variables:
                ci = ci.replace(ciVariableSet[i], cjVariableSet[i])
                remove_spot.append(cjVariableSet[i])

        for i in remove_spot:
            cjVariableSet.remove(i)

        for i in range(len(cjVariableSet)):
            if cjVariableSet[i] in Variables:
                cj = cj.replace(cjVariableSet[i], ciVariableSet[i])
        return ci, cj

    elif ci.find(",") != -1:
        return ci, cj

    elif cj.find(",") != -1:
        return ci, cj

    else:
        ciVariable = ci[ci.find('(') + 1:ci.rfind(')')]
        cjVariable = cj[cj.find('(') + 1:cj.rfind(')')]

        if bracketsCountFor(ci) == 2 and bracketsCountFor(cj) == 2:  # only one variable or const
            if ciVariable in Variables:
                ci = ci.replace(ciVariable, cjVariable)
            elif cjVariable in Variables:
                cj = cj.replace(cjVariable, ciVariable)
            return ci, cj

        else:
            if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:

                x_function = ci[ci.find('(') + 1:ci.rfind(')')]
                y_function = cj[cj.find('(') + 1:cj.rfind(')')]

                if x_function.split("(")[0] in Functions:
                    ciVariable = x_function[x_function.find('(') + 1:x_function.rfind(')')]
                    cjVariable = y_function[y_function.find('(') + 1:y_function.rfind(')')]
                    if ciVariable in Variables:
                        ci = ci.replace(ciVariable, cjVariable)
                    elif cjVariable in Variables:
                        cj = cj.replace(cjVariable, ciVariable)
                return ci, cj

            elif bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 2:

                x_function = ci[ci.find('(') + 1:ci.rfind(')')]
                if x_function.split("(")[0] in Functions:
                    cjVariable = cj[cj.find('(') + 1:cj.rfind(')')]
                    if cjVariable in Variables:
                        cj = cj.replace(cjVariable, x_function)
                return ci, cj
            else:
                y_function = cj[cj.find('(') + 1:cj.rfind(')')]
                if y_function.split("(")[0] in Functions:
                    ciVariable = ci[ci.find('(') + 1:ci.rfind(')')]
                    if ciVariable in Variables:
                        ci = ci.replace(ciVariable, y_function)
                return ci, cj


def negationOf(clause):
    if clause.find("!") != -1:
        clause = clause.replace("!", "")
    else:
        clause = "!" + clause[0:]
    return clause


def plResolve(ci, cj):  # return all possibility from two Clauses
    """
    returns all clauses that can be obtained from clauses ci and cj
    """
    clauses = []
    ciOriginal = ci.split(" ")
    cjOriginal = cj.split(" ")
    for i in ciOriginal:
        for j in cjOriginal:
            iUnified, jUnified = unify(i, j)  # Unify two to see if it can be same
            if iUnified == negationOf(jUnified) or negationOf(iUnified) == jUnified:  #
                ciTemp = ci.split(" ")
                ciTemp.remove(i)
                cjTemp = cj.split(" ")
                cjTemp.remove(j)

                ciNew = ""
                cjNew = ""

                spaceBetweenClauses = ""
                if len(ciTemp) > 1:
                    spaceBetweenClauses = " "
                for item in ciTemp:
                    if ciNew != "":
                        ciNew = ciNew + spaceBetweenClauses + item
                    else:
                        ciNew = ciNew + item

                spaceBetweenClauses = ""
                if len(cjTemp) > 1:
                    spaceBetweenClauses = " "
                for item in cjTemp:
                    if cjNew != "":
                        cjNew = cjNew + spaceBetweenClauses + item
                    else:
                        cjNew = cjNew + item

                if ciNew == "" and cjNew == "":
                    clauses.append([])
                else:
                    if cjNew == "" or ciNew == "":
                        clauses.append(ciNew + cjNew)
                    else:
                        clauses.append(ciNew + " " + cjNew)
    return clauses


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





if len(sys.argv) < 1:
    print("Invalid number of arguments!")
    sys.exit(1)
else:
    with open("/Users/abhishekshah/Documents/Spring 22/Ass-AI-630/AI Lab2/testcases/functions/f5.cnf") as f:
        lines = f.readlines()
        Predicates = lines[0].split()[1:]
        Variables = lines[1].split()[1:]
        Constants = lines[2].split()[1:]
        Functions = lines[3].split()[1:]
        for i in range(5, len(lines)):
            Clauses.append(lines[i].strip().rstrip('\n'))

if plResolution(Clauses):
    print("no")
else:
    print("yes")
