from os import remove, replace, truncate
import sys
import re

Predicates = []
Variables = []
Constants = []
Functions = []
Clauses = []

def bracketsCountFor(x):
    brackets = 0
    for i in x:
        if i == "(" or i == ")":
            brackets += 1
    return brackets


def negationOf(a):
    if a.find("!") != -1:
        a = a.replace("!", "")
    else:
        a = "!" + a[0:]
    return a


def parseDataFor(ci, cj):
    ciVariable = ci[ci.find('(') + 1:ci.rfind(')')]
    cjVariable = cj[cj.find('(') + 1:cj.rfind(')')]
    x_term_set = ciVariable.split(",")
    y_term_set = cjVariable.split(",")

    if bracketsCountFor(ci) != 4 and bracketsCountFor(cj) == 4:
        for i in range(0, len(x_term_set)):
            if x_term_set[i] in Variables:
                ci = ci.replace(x_term_set[i], y_term_set[i])
        return ci, cj
    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) != 4:
        for i in range(0, len(y_term_set)):
            if y_term_set[i] in Variables:
                cj = cj.replace(y_term_set[i], x_term_set[i])
        return ci, cj

    if bracketsCountFor(ci) == 4 and bracketsCountFor(cj) == 4:
        for i in range(0, len(x_term_set)):
            if x_term_set[i].find("(") != -1:
                x_function = x_term_set[i]
                y_function = y_term_set[i]
                if x_function.split("(")[0] in Functions:
                    x_var = x_function[x_function.find('(') + 1:x_function.rfind(')')]
                    y_var = y_function[y_function.find('(') + 1:y_function.rfind(')')]
                    if x_var in Variables:
                        ci = ci.replace(x_var, y_var)
                    elif y_var in Variables:
                        cj = cj.replace(y_var, x_var)

                return ci, cj

    return ci, cj


def unify(ci, cj):
    if ci.find(",") != -1 and cj.find(",") != -1:
        if bracketsCountFor(ci) == 4 or bracketsCountFor(cj) == 4:
            ci, cj = parseDataFor(ci, cj)
        ciVariable = ci[ci.find('(') + 1:ci.rfind(')')]
        cjVariable = cj[cj.find('(') + 1:cj.rfind(')')]
        ciVariableSet = ciVariable.split(",")
        cjVariableSet = cjVariable.split(",")
        remove_spot = []
        for i in range(0, len(ciVariableSet)):
            if ciVariableSet[i] in Variables:
                ci = ci.replace(ciVariableSet[i], cjVariableSet[i])
                remove_spot.append(cjVariableSet[i])
        for i in remove_spot:
            cjVariableSet.remove(i)
        for i in range(0, len(cjVariableSet)):
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


def plResolve(C1, C2):  # retrun all possibility from two Clauses
    resolvents = []
    ciOriginal = C1.split(" ")
    cjOriginal = C2.split(" ")
    for i in ciOriginal:
        for j in cjOriginal:
            iUnified, jUnified = unify(i, j)  # Unify two to see if it can be same
            if iUnified == negationOf(jUnified) or negationOf(iUnified) == jUnified:  #
                ciTemp = C1.split(" ")
                ciTemp.remove(i)
                cjTemp = C2.split(" ")
                cjTemp.remove(j)
                itmp = ""
                jtmp = ""
                char_space = ""
                if len(ciTemp) >= 2:
                    char_space = " "
                for i in ciTemp:
                    if itmp != "":
                        itmp = itmp + char_space + i
                    else:
                        itmp = itmp + i

                char_space = ""
                if len(cjTemp) >= 2:
                    char_space = " "

                for j in cjTemp:
                    if jtmp != "":
                        jtmp = jtmp + char_space + j
                    else:
                        jtmp = jtmp + j

                if itmp == "" and jtmp == "":
                    resolvents.append([])
                else:
                    if jtmp == "" or itmp == "":
                        resolvents.append(itmp + jtmp)
                    else:
                        resolvents.append(itmp + " " + jtmp)

    return resolvents


def subsetOf(list1, list2):
    for item in list1:
        if item not in list2:
            return False
    return True


def plResolution(Clauses_set):  # resolution function return true or false
    # print(Clauses_set)
    newList = []
    while True:
        allPairs = [(Clauses_set[i], Clauses_set[j]) for i in range(len(Clauses_set)) for j in
                 range(i + 1, len(Clauses_set))]  # make pair from all possible Clauses
        for (ci, cj) in allPairs:
            resolvents = plResolve(ci, cj)  # Call Resolver
            # print(resolvents)
            if [] in resolvents:  # if the empty Clauses we return T
                return True
            for temp in resolvents:
                if temp not in newList:
                    newList.append(temp)
        if subsetOf(newList, Clauses_set):  # check if the sublist we return false
            return False
        for i in newList:
            if i not in Clauses_set:
                Clauses_set.append(i)


with open("/Users/abhishekshah/Documents/Spring 22/Ass-AI-630/AI Lab2/testcases/universals+constants/uc09.cnf") as f:  # read all the data from the file
    line_cnf = f.readline()
    while line_cnf:  # read line by line and store into the list
        if line_cnf.find("Predicates:") != (-1):
            line_cnf = line_cnf.replace("Predicates: ", "")
            Predicates = line_cnf.strip().split(" ")
            if Predicates[0] == "":
                Predicates = []
            line_cnf = ""
        if line_cnf.find("Variables:") != (-1):
            line_cnf = line_cnf.replace("Variables: ", "")
            Variables = line_cnf.strip().split(" ")
            if Variables[0] == "":
                Variables = []
            line_cnf = ""
        if line_cnf.find("Constants:") != (-1):
            line_cnf = line_cnf.replace("Constants: ", "")
            Constants = line_cnf.strip().split(" ")
            if Constants[0] == "":
                Constants = []
            line_cnf = ""
        if line_cnf.find("Functions:") != (-1):
            line_cnf = line_cnf.replace("Functions: ", "")
            Functions = line_cnf.strip().split(" ")
            if Functions[0] == "":
                Functions = []
            line_cnf = ""
        line_cnf = line_cnf.replace("Clauses:", "")
        line_cnf = line_cnf.strip()
        if line_cnf != "":
            Clauses.append(line_cnf)
        line_cnf = f.readline()


if plResolution(Clauses):
    print("no")
else:
    print("yes")
