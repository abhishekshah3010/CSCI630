import math
from treeNode import *
from checkFeatures import *
import pickle


def calculateEntropy(value):
    """
    Entropy function
    :param value:Input value
    :return:Calculate entropy and return
    """
    if value == 1:
        return 0
    entropy = (-1) * (value * math.log(value, 2.0) + (1 - value) * math.log((1 - value), 2.0))
    return entropy


def appendFeatures(allSentences):
    """
    Creates features list
    """
    feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8 = ([] for _ in range(8))

    # Based on the sentences fill the values for the features
    for line in allSentences:
        feature1.append(commonDutchWords(line))
        feature2.append(commonEnglishWords(line))
        feature3.append(englishArticles(line))
        feature4.append(checkAvgLenGreaterThan5(line))
        feature5.append(containsX(line))
        feature6.append(enWord(line))
        feature7.append(stringVan(line))
        feature8.append(stringDeHet(line))

    features = [feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8]

    return features


def dtPredict(hypothesis, file):
    """
    Predicts for the decision tree
    """

    # Load already saved(while training) decision tree model
    loadModel = pickle.load(open(hypothesis, 'rb'))
    testDataFile = open(file)
    allStatements = []
    sentence = ""
    wordCounter = 0

    # Grab 15-word sentence from the testData file
    for line in testDataFile:
        words = line.split()

        for word in words:
            if wordCounter != 14:
                sentence = sentence + word + " "
                wordCounter = wordCounter + 1
            else:
                sentence = sentence + word
                allStatements.append(sentence)
                sentence = ""
                wordCounter = 0

    features = appendFeatures(allStatements)

    statementCounter = 0
    # For every statement run through the decision tree to find out the langauge for the examples
    for sentence in allStatements:
        model = loadModel
        while type(model.value) != str:
            value = features[model.value][statementCounter]
            if value:
                model = model.left
            else:
                model = model.right
        print(model.value)
        statementCounter = statementCounter + 1


def number_of_diff_values(values, total):
    """
    To check for total positive or total negative examples in a set
    :param values:Input set
    :param total:Indices
    :return:Return based on whether total negative or positive examples
    """
    value = values[total[0]]
    for i in total:
        if value != values[i]:
            return 10
    return 0


def collect_data_dt(exampleFile, hypothesisFile):
    """
    Collection of data and calling the required functions
    :param exampleFile:Training file
    :param hypothesisFile:File to which hypothesis is to be written
    """
    trainData = open(exampleFile, 'r')
    allData = ""
    for lines in trainData:
        allData = allData + lines

    # get all the data in the file
    allStatements = allData.split('|')
    countAllStatements = len(allStatements)
    allWords = allData.split()

    for i in range(countAllStatements):
        if i < 1:
            continue
        allStatements[i] = allStatements[i][:-4]
    allStatements = allStatements[1:]

    # Get all the language label(en or nl)
    languageLabel = []
    index = 0
    for word in allWords:
        if word.startswith('nl|') or word.startswith('en|'):
            languageLabel.insert(index, word[:2])
            index = index + 1

    features = appendFeatures(allStatements)
    number_lst = [i for i in range(len(languageLabel))]

    # To keep track of features visited along the sentence
    visited = []
    rootNode = tree(features, None, languageLabel, number_lst, 0, None, None)

    # Calling decision tree function here
    dtTrain(rootNode, features, visited, languageLabel, number_lst, 0, None)

    # Saving/Dumping the hypothesisFile
    saveModel = open(hypothesisFile, 'wb')
    pickle.dump(rootNode, saveModel)


def dtTrain(rootNode, features, visited, results, total_results, depth, prevLevelPrediction):
    """
    Decides on the best splitting attribute for a given depth , make a node for that and connects it with
    two nodes containing the left and right childs for the given so called root node
    :param rootNode: The node that is being considered right now
    :param features:Total set of attributes and their values
    :param visited:Every node that has been seen till now
    :param results:Final results in a list
    :param total_results:Index of examples that are there at this level
    :param depth:Level in consideration
    :param prevLevelPrediction:Prediction made before this depth
    :return:None
    """

    # If depth is reached return the plurality of the remaining set
    if depth == len(features) - 1:
        enLabel = 0
        nlLabel = 0
        for index in total_results:
            if results[index] == 'en':
                enLabel += 1
            elif results[index] == 'nl':
                nlLabel += 1
        if enLabel > nlLabel:
            rootNode.value = 'en'
            print("en")
        else:
            rootNode.value = 'nl'
            print("nl")

    # If there are no examples left return the prediction made at the previous level
    elif len(total_results) == 0:
        rootNode.value = prevLevelPrediction
        print(prevLevelPrediction)

    # If there are only positive or only negative examples left return the prediction directly from the plurality
    elif number_of_diff_values(results, total_results) == 0:
        rootNode.value = results[total_results[0]]
        print(results[total_results[0]])

    # If all the attributes have been used for splitting along a given path return the prediction of the set of examples
    elif len(features) == len(visited):
        enLabel = 0
        nlLabel = 0
        for index in total_results:
            if results[index] == 'en':
                enLabel = enLabel + 1
            elif results[index] == 'nl':
                nlLabel = nlLabel + 1
        if enLabel > nlLabel:
            rootNode.value = 'en'
        else:
            rootNode.value = 'nl'

    # Find the attribute to split on
    else:
        gain = []
        results_en = 0
        results_nl = 0

        # Take the total number of positive and negative examples at this level
        for index in total_results:
            if results[index] == 'en':
                results_en = results_en + 1
            else:
                results_nl = results_nl + 1
        # For each attribute
        for index_attribute in range(len(features)):

            # Check if it has already been used for splitting so , no gain in splitting over it again
            if index_attribute in visited:
                gain.append(0)
                continue

            # Else see for the best splitting attribute
            else:
                count_true_en = 0
                count_true_nl = 0
                count_false_en = 0
                count_false_nl = 0

                for index in total_results:

                    if features[index_attribute][index] is True and results[index] == 'en':
                        count_true_en = count_true_en + 1
                    elif features[index_attribute][index] is True and results[index] == 'nl':
                        count_true_nl = count_true_nl + 1
                    elif features[index_attribute][index] is False and results[index] == 'en':
                        count_false_en = count_false_en + 1
                    elif features[index_attribute][index] is False and results[index] == 'nl':
                        count_false_nl = count_false_nl + 1

                # If only positive or only negative examples remain at a particular point , no point in splitting
                if (count_true_nl + count_true_en == 0) or (count_false_en + count_false_nl == 0):
                    gain_for_attribute = 0
                    gain.append(gain_for_attribute)
                    continue
                # Handliing certain outlier conditions
                if count_true_en == 0:
                    rem_true_value = 0
                    # rem_false_value = 0
                    rem_false_value = (
                                              (count_false_en + count_false_nl) / (results_nl + results_nl)) * calculateEntropy(
                        count_false_en / (count_false_nl + count_false_en))
                elif count_false_en == 0:
                    rem_false_value = 0
                    # rem_true_value = 0
                    rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * calculateEntropy(
                        count_true_en / (count_true_nl + count_true_en))
                else:
                    rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * calculateEntropy(
                        count_true_en / (count_true_nl + count_true_en))

                    rem_false_value = (
                                              (count_false_en + count_false_nl) / (results_nl + results_en)) * calculateEntropy(
                        count_false_en / (count_false_nl + count_false_en))

                # Find the gain for each attribute
                gain_for_attribute = calculateEntropy(results_en / (results_en + results_nl)) - (rem_true_value +
                                                                                                 rem_false_value)
                gain.append(gain_for_attribute)

        # Check if the max gain is 0 then return back as no more gain possible along this path
        if max(gain) == 0:
            rootNode.value = prevLevelPrediction
            print(rootNode.value)
            return

        # Select the max gain attribute
        max_gain_attribute = gain.index(max(gain))

        visited.append(max_gain_attribute)

        index_True = []
        index_False = []

        # Separate out true and false portion for the found out max gain attribute
        for index in total_results:
            if features[max_gain_attribute][index] is True:
                index_True.append(index)
            else:
                index_False.append(index)

        # Prediction at this stage
        prediction_at_this_stage = ''

        if results_en > results_nl:
            prediction_at_this_stage = 'en'
        else:
            prediction_at_this_stage = 'nl'

        bool_false = False
        bool_true = True
        rootNode.value = max_gain_attribute

        # Make left portion for the max gain attribute
        left_obj = tree(features, None, results, index_True, depth + 1,
                        prediction_at_this_stage, bool_true)
        # Make right portion for the max gain attribute
        right_obj = tree(features, None, results, index_False, depth + 1,
                         prediction_at_this_stage, bool_false)
        rootNode.left = left_obj
        rootNode.right = right_obj
        # Recurse left and right portions
        dtTrain(left_obj, features, visited, results, index_True, depth + 1, prediction_at_this_stage)
        dtTrain(right_obj, features, visited, results, index_False, depth + 1, prediction_at_this_stage)

        del visited[-1]
