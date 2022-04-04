import math

file1 = open('data.txt', 'r')
Lines = file1.readlines()

infoGain = []
for i in range(8):
    aTrue = 0
    aFalse = 0
    bTrue = 0
    bFalse = 0
    countA = 0
    countB = 0

    for line in Lines:
        x = line.split()
        if x[8] == 'A':
            countA += 1
            if x[i] == 'False':
                aFalse += 1
            else:
                aTrue += 1
        else:
            countB += 1
            if x[i] == 'False':
                bFalse += 1
            else:
                bTrue += 1

    pTrue = (aTrue + bTrue) / (aTrue + bTrue + aFalse + bFalse)
    pFalse = (aFalse + bFalse) / (aTrue + bTrue + aFalse + bFalse)

    entropyTrue = -((aTrue / (aTrue + bTrue)) * math.log((aTrue / (aTrue + bTrue)), 2)) - ((bTrue / (aTrue + bTrue)) * math.log((bTrue / (aTrue + bTrue)), 2))

    entropyFalse = -((aFalse / (aFalse + bFalse)) * math.log((aFalse / (aFalse + bFalse)), 2)) - ((bFalse / (aFalse + bFalse)) * math.log((bFalse / (aFalse + bFalse)), 2))

    entropyA = (pTrue * entropyTrue) + (pFalse * entropyFalse)

    entropyWhole = -(((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)), 2)) - (((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)), 2))

    infoGain.append(entropyWhole - entropyA)
    print('Attribute', i + 1, '\n\naTrue = ', aTrue, '\naFalse = ', aFalse, '\nbTrue = ', bTrue, '\nbFalse = ', bFalse, '\npTrue = ', pTrue, '\npFalse = ', pFalse, '\nentropyTrue = ', entropyTrue, '\nentropyFalse = ', entropyFalse, '\nentropyA = ', entropyA, '\nentropyWhole = ', entropyWhole, '\n\n********************************\n\n')

print('infoGain =\t', infoGain, '\nmax(infoGain) =\t', max(infoGain), '\n', infoGain.index(max(infoGain)) + 1, 'th attribute among given 8 attributes has highest information gain')
print('countA = ', countA, '\ncountB = ', countB, '\n\n********************************\n\n')


infoGainLvl1True = []
for i in range(8):
    if i == 3:
        continue
    else:
        aTrue = 0
        aFalse = 0
        bTrue = 0
        bFalse = 0
        countA = 0
        countB = 0
        for line in Lines:
            x = line.split()
            if x[3] == 'True':
                if x[8] == 'A':
                    countA += 1
                    if x[i] == 'False':
                        aFalse += 1
                    else:
                        aTrue += 1
                else:
                    countB += 1
                    if x[i] == 'False':
                        bFalse += 1
                    else:
                        bTrue += 1

    pTrue = (aTrue + bTrue) / (aTrue + bTrue + aFalse + bFalse)
    pFalse = (aFalse + bFalse) / (aTrue + bTrue + aFalse + bFalse)
    entropyTrue = -((aTrue / (aTrue + bTrue)) * math.log((aTrue / (aTrue + bTrue)), 2)) - ((bTrue / (aTrue + bTrue)) * math.log((bTrue / (aTrue + bTrue)), 2))
    entropyFalse = -((aFalse / (aFalse + bFalse)) * math.log((aFalse / (aFalse + bFalse)), 2)) - ((bFalse / (aFalse + bFalse)) * math.log((bFalse / (aFalse + bFalse)), 2))
    entropyA = (pTrue * entropyTrue) + (pFalse * entropyFalse)
    entropyWhole = -(((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)), 2)) - (((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)), 2))
    infoGainLvl1True.append(entropyWhole - entropyA)
    print('Attribute', i + 1, '\n\naTrue = ', aTrue, '\naFalse = ', aFalse, '\nbTrue = ', bTrue, '\nbFalse = ', bFalse, '\npTrue = ', pTrue, '\npFalse = ', pFalse, '\nentropyTrue = ', entropyTrue, '\nentropyFalse = ', entropyFalse, '\nentropyA = ', entropyA, '\nentropyWhole = ', entropyWhole, '\n\n********************************\n\n')

print('infoGainLvl1True =\t', infoGainLvl1True, '\nmax(infoGainLvl1True) =\t', max(infoGainLvl1True), '\n', infoGainLvl1True.index(max(infoGainLvl1True)) + 2, 'th attribute among given 8 attributes has highest information gain\n')
print('countATrue = ', countA, '\ncountBTrue = ', countB, '\n\n********************************\n\n')

infoGainLvl1False = []
for i in range(8):
    if i == 3:
        continue
    else:
        aTrue = 0
        aFalse = 0
        bTrue = 0
        bFalse = 0
        countA = 0
        countB = 0

        for line in Lines:
            x = line.split()
            if x[3] == 'False':
                if x[8] == 'A':
                    countA += 1
                    if x[i] == 'False':
                        aFalse += 1
                    else:
                        aTrue += 1
                else:
                    countB += 1
                    if x[i] == 'False':
                        bFalse += 1
                    else:
                        bTrue += 1

    pTrue = (aTrue + bTrue) / (aTrue + bTrue + aFalse + bFalse)
    pFalse = (aFalse + bFalse) / (aTrue + bTrue + aFalse + bFalse)
    entropyTrue = -((aTrue / (aTrue + bTrue)) * math.log((aTrue / (aTrue + bTrue)), 2)) - (
                (bTrue / (aTrue + bTrue)) * math.log((bTrue / (aTrue + bTrue)), 2))
    entropyFalse = -((aFalse / (aFalse + bFalse)) * math.log((aFalse / (aFalse + bFalse)), 2)) - (
                (bFalse / (aFalse + bFalse)) * math.log((bFalse / (aFalse + bFalse)), 2))
    entropyA = (pTrue * entropyTrue) + (pFalse * entropyFalse)
    entropyWhole = -(((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(
        ((aTrue + aFalse) / (aTrue + bTrue + aFalse + bFalse)), 2)) - (
                               ((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)) * math.log(
                           ((bTrue + bFalse) / (aTrue + bTrue + aFalse + bFalse)), 2))
    infoGainLvl1False.append(entropyWhole - entropyA)
    print('Attribute', i + 1, '\n\naTrue = ', aTrue, '\naFalse = ', aFalse, '\nbTrue = ', bTrue, '\nbFalse = ', bFalse, '\npTrue = ', pTrue, '\npFalse = ', pFalse, '\nentropyTrue = ', entropyTrue, '\nentropyFalse = ', entropyFalse, '\nentropyA = ', entropyA, '\nentropyWhole = ', entropyWhole, '\n\n********************************\n\n')

print('infoGainLvl1False =\t', infoGainLvl1False, '\nmax(infoGainLvl1False) =\t', max(infoGainLvl1False), '\n', infoGainLvl1False.index(max(infoGainLvl1False)) + 2, 'th attribute among given 8 attributes has highest information gain\n')
print('countAFalse = ', countA, '\ncountBFalse = ', countB, '\n\n********************************\n\n')