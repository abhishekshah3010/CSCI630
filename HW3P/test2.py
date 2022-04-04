import math

file1 = open('data.txt', 'r')
data = file1.readlines()

informationGain = []
print("Root node (Level 0)")
for i in range(8):
    ATrue = 0
    AFalse = 0
    BTrue = 0
    BFalse = 0
    Acount = 0
    Bcount = 0

    for line in data:
        x = line.split()
        if x[8] == 'A':
            Acount += 1
            if x[i] == 'False':
                AFalse += 1
            else:
                ATrue += 1
        else:
            Bcount += 1
            if x[i] == 'False':
                BFalse += 1
            else:
                BTrue += 1

    trueProbability = (ATrue + BTrue) / (ATrue + BTrue + AFalse + BFalse)
    falseProbability = (AFalse + BFalse) / (ATrue + BTrue + AFalse + BFalse)

    trueEntropy = -((ATrue / (ATrue + BTrue)) * math.log((ATrue / (ATrue + BTrue)), 2)) - ((BTrue / (ATrue + BTrue)) * math.log((BTrue / (ATrue + BTrue)), 2))

    falseEntropy = -((AFalse / (AFalse + BFalse)) * math.log((AFalse / (AFalse + BFalse)), 2)) - ((BFalse / (AFalse + BFalse)) * math.log((BFalse / (AFalse + BFalse)), 2))

    remainderA = (trueProbability * trueEntropy) + (falseProbability * falseEntropy)

 
    informationGain.append(entropyAttribute - remainderA)
    print('Attribute number:', i + 1, '\n\nATrue = ', ATrue, '\nBTrue = ', BTrue, '\nAFalse = ', AFalse, '\nBFalse = ',
          BFalse, '\nTrue Probability = ', trueProbability, '\nFalse Probability = ', falseProbability,
          '\nTrue Entropy = ', trueEntropy, '\nFalse Entropy = ', falseEntropy, '\nRemainder A = ', remainderA,
          '\nEntropy Attribute = ', entropyAttribute, '\n------------------------------------------------')
print('A count = ', Acount, '\tB count = ', Bcount)
print('Information gain =', informationGain, '\nMaximum of information gain =', max(informationGain))
print()
print(informationGain.index(max(informationGain)) + 1,
      'th attribute will be the root node which is nothin but level 0.')
print('\n------------------------------------------------\n\n')

print("True node split (Level 1)")
infoGainLvl1True = []
for i in range(8):
    if i == 3:
        continue
    else:
        ATrue = 0
        AFalse = 0
        BTrue = 0
        BFalse = 0
        Acount = 0
        Bcount = 0
        for line in data:
            x = line.split()
            if x[3] == 'True':
                if x[8] == 'A':
                    Acount += 1
                    if x[i] == 'False':
                        AFalse += 1
                    else:
                        ATrue += 1
                else:
                    Bcount += 1
                    if x[i] == 'False':
                        BFalse += 1
                    else:
                        BTrue += 1

    trueProbability = (ATrue + BTrue) / (ATrue + BTrue + AFalse + BFalse)
    falseProbability = (AFalse + BFalse) / (ATrue + BTrue + AFalse + BFalse)
    trueEntropy = -((ATrue / (ATrue + BTrue)) * math.log((ATrue / (ATrue + BTrue)), 2)) - ((BTrue / (ATrue + BTrue)) * math.log((BTrue / (ATrue + BTrue)), 2))
    falseEntropy = -((AFalse / (AFalse + BFalse)) * math.log((AFalse / (AFalse + BFalse)), 2)) - ((BFalse / (AFalse + BFalse)) * math.log((BFalse / (AFalse + BFalse)), 2))
    remainderA = (trueProbability * trueEntropy) + (falseProbability * falseEntropy)
    entropyAttribute = -(((ATrue + AFalse) / (ATrue + BTrue + AFalse + BFalse)) * math.log(((ATrue + AFalse) / (ATrue + BTrue + AFalse + BFalse)), 2)) - (((BTrue + BFalse) / (ATrue + BTrue + AFalse + BFalse)) * math.log(((BTrue + BFalse) / (ATrue + BTrue + AFalse + BFalse)), 2))
    infoGainLvl1True.append(entropyAttribute - remainderA)
    print('Attribute number:', i + 1, '\n\nATrue = ', ATrue, '\nBTrue = ', BTrue, '\nAFalse = ', AFalse, '\nBFalse = ',
          BFalse, '\nTrue Probability = ', trueProbability, '\nFalse Probability = ', falseProbability,
          '\nTrue Entropy = ', trueEntropy, '\nFalse Entropy = ', falseEntropy, '\nRemainder A = ', remainderA,
          '\nEntropy Attribute = ', entropyAttribute, '\n------------------------------------------------')
print('A True count = ', Acount, '\tB True count = ', Bcount)
print('Information gain =', informationGain, '\nMaximum of information gain =', max(infoGainLvl1True))
print()
print(infoGainLvl1True.index(max(infoGainLvl1True)) + 2,
      'th attribute will be the node of True split of the root node which will be at level 2.')
print('\n------------------------------------------------\n\n')

print("False node split (Level 1)")
infoGainLvl1False = []
for i in range(8):
    if i == 3:
        continue
    else:
        ATrue = 0
        AFalse = 0
        BTrue = 0
        BFalse = 0
        Acount = 0
        Bcount = 0

        for line in data:
            x = line.split()
            if x[3] == 'False':
                if x[8] == 'A':
                    Acount += 1
                    if x[i] == 'False':
                        AFalse += 1
                    else:
                        ATrue += 1
                else:
                    Bcount += 1
                    if x[i] == 'False':
                        BFalse += 1
                    else:
                        BTrue += 1

    trueProbability = (ATrue + BTrue) / (ATrue + BTrue + AFalse + BFalse)
    falseProbability = (AFalse + BFalse) / (ATrue + BTrue + AFalse + BFalse)
    trueEntropy = -((ATrue / (ATrue + BTrue)) * math.log((ATrue / (ATrue + BTrue)), 2)) - (
            (BTrue / (ATrue + BTrue)) * math.log((BTrue / (ATrue + BTrue)), 2))
    falseEntropy = -((AFalse / (AFalse + BFalse)) * math.log((AFalse / (AFalse + BFalse)), 2)) - (
            (BFalse / (AFalse + BFalse)) * math.log((BFalse / (AFalse + BFalse)), 2))
    remainderA = (trueProbability * trueEntropy) + (falseProbability * falseEntropy)
    entropyAttribute = -(((ATrue + AFalse) / (ATrue + BTrue + AFalse + BFalse)) * math.log(
        ((ATrue + AFalse) / (ATrue + BTrue + AFalse + BFalse)), 2)) - (
                           ((BTrue + BFalse) / (ATrue + BTrue + AFalse + BFalse)) * math.log(
                           ((BTrue + BFalse) / (ATrue + BTrue + AFalse + BFalse)), 2))
    infoGainLvl1False.append(entropyAttribute - remainderA)
    print('Attribute number:', i + 1, '\n\nATrue = ', ATrue, '\nBTrue = ', BTrue, '\nAFalse = ', AFalse, '\nBFalse = ',
          BFalse, '\nTrue Probability = ', trueProbability, '\nFalse Probability = ', falseProbability,
          '\nTrue Entropy = ', trueEntropy, '\nFalse Entropy = ', falseEntropy, '\nRemainder A = ', remainderA,
          '\nEntropy Attribute = ', entropyAttribute, '\n------------------------------------------------')
print('A False count = ', Acount, '\tB False count = ', Bcount)
print('Information gain =', informationGain, '\nMaximum of information gain =', max(infoGainLvl1False))
print()
print(infoGainLvl1False.index(max(infoGainLvl1False)) + 2,
      'th attribute will be the node of False split of the root node which will be at level 2.')