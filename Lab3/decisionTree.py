import math
from treeNode import *
from checkFeatures import *
import pickle


def readTrainingData(trainingDataFile):
    """
    Read data from the train.dat file for training
    :param trainingDataFile:input training file
    :return:list of statements and final predictions
    """

    # open file
    file = open(trainingDataFile)
    allData = ""
    for lines in file:
        allData = allData + lines

    # get all the statements
    allStatements = allData.split('|')
    all_data_stripped_space = allData.split()

    for i in range(len(allStatements)):
        if i < 1:
            continue
        allStatements[i] = allStatements[i][:-4]
    allStatements = allStatements[1:]

    # Get all the results
    languageLabel = []
    index = 0
    for values in all_data_stripped_space:
        if values.startswith('nl|') or values.startswith('en|'):
            languageLabel.insert(index, values[0:2])
            index = index + 1
    #
    return allStatements, languageLabel


def entropy(value):
    """
    Entropy function
    :param value:Input value
    :return:Calculate entropy and return
    """
    if value == 1:
        return 0
    return (-1) * (value * math.log(value, 2.0) + (1 - value) * math.log((1 - value), 2.0))


def appendFeatures(sentence_list):
    feature1, feature2, feature3, feature4, feature5, feature6, feature7, \
    feature8, feature9, feature10, feature11 = ([] for i in range(11))

    # Based on the sentences fill the values for the attributes
    for line in sentence_list:
        feature1.append(containsQ(line))
        feature2.append(containsX(line))
        feature3.append(check_avg_word_length_greater_than_5(line))
        feature4.append(presence_of_van(line))
        feature5.append(presence_of_de_het(line))
        feature6.append(check_for_een(line))
        feature7.append(check_for_en(line))
        feature8.append(check_for_common_dutch_words(line))
        feature9.append(check_for_common_english_words(line))
        feature10.append(presence_of_a_an_the(line))
        feature11.append(check_presence_of_and(line))

    attributes = [feature1, feature2, feature3, feature4, feature5, feature6, feature7, feature8,
                  feature9, feature10, feature11]

    return attributes


def predict_dt(hypothesis, file):
    """
    Does the prediction for the decision tree
    :param hypothesis:Input decision tree
    :param file:Input test file
    :return:None
    """

    # Load decision tree model
    object = pickle.load(open(hypothesis, 'rb'))
    file_open = open(file)
    sentence_list = []
    counter = 0
    sentence = ''

    # Extract 15-word samples from the test file
    for line in file_open:
        words = line.split()

        for word in words:
            if counter != 14:
                sentence += word + ' '
                counter += 1
            else:
                sentence += word
                sentence_list.append(sentence)
                sentence = ''
                counter = 0

    attributes = appendFeatures(sentence_list)

    statement = 0
    # For every statement run through the decision tree to find out the langauge for the examples
    for sentence in sentence_list:
        object_temp = object
        while type(object_temp.value) != str:
            value = attributes[object_temp.value][statement]
            if value is True:
                object_temp = object_temp.left
            else:
                object_temp = object_temp.right
        print(object_temp.value)
        statement = statement + 1


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

    statements, results = readTrainingData(exampleFile)

    attributes = appendFeatures(statements)

    number_lst = []
    for i in range(len(results)):
        number_lst.append(i)

    # To keep track of attributes splitted along a path
    seen = []
    root = tree(attributes, None, results, number_lst, 0, None, None)

    # Calling decision tree function here
    value = train_decision_tree(root, attributes, seen, results, number_lst, 0, None)

    # Dumping the hypothesis to a file using pickle
    filehandler = open(hypothesisFile, 'wb')
    pickle.dump(root, filehandler)


def check_for_0_gain(values):
    """
    If 0 gain then return
    :param values:values of gain for the level
    :return:False if the max gain is 0
    """
    if max(values) == 0:
        return False


def train_decision_tree(root, attributes, seen, results, total_results, depth, prevprediction):
    """
    Decides on the best splitting attribute for a given depth , make a node for that and connects it with
    two nodes containing the left and right childs for the given so called root node
    :param root: The node that is being considered right now
    :param attributes:Total set of attributes and their values
    :param seen:Every node that has been seen till now
    :param results:Final results in a list
    :param total_results:Index of examples that are there at this level
    :param depth:Level in consideration
    :param prevprediction:Prediction made before this depth
    :return:None
    """

    # If depth is reached return the plurality of the remaining set
    if depth == len(attributes) - 1:
        counten = 0
        countnl = 0
        for index in total_results:
            if results[index] == 'en':
                counten = counten + 1
            elif results[index] == 'nl':
                countnl = countnl + 1
        if counten > countnl:
            root.value = 'en'
            print('en')
        else:
            root.value = 'nl'
            print('nl')

    # If there are no examples left return the prediction made at the previous level
    elif len(total_results) == 0:
        root.value = prevprediction
        print(prevprediction)

    # If there are only positive or only negative examples left return the prediction directly from the plurality
    elif number_of_diff_values(results, total_results) == 0:
        root.value = results[total_results[0]]
        print(results[total_results[0]])

    # If all the attributes have been used for splitting along a given path return the prediction of the set of examples
    elif len(attributes) == len(seen):
        counten = 0
        countnl = 0
        for index in total_results:
            if results[index] == 'en':
                counten = counten + 1
            elif results[index] == 'nl':
                countnl = countnl + 1
        if counten > countnl:
            root.value = 'en'
        else:
            root.value = 'nl'

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
        for index_attribute in range(len(attributes)):

            # Check if it has already been used for splitting so , no gain in splitting over it again
            if index_attribute in seen:
                gain.append(0)
                continue

            # Else see for the best splitting attribute
            else:
                count_true_en = 0
                count_true_nl = 0
                count_false_en = 0
                count_false_nl = 0

                for index in total_results:

                    if attributes[index_attribute][index] is True and results[index] == 'en':
                        count_true_en = count_true_en + 1
                    elif attributes[index_attribute][index] is True and results[index] == 'nl':
                        count_true_nl = count_true_nl + 1
                    elif attributes[index_attribute][index] is False and results[index] == 'en':
                        count_false_en = count_false_en + 1
                    elif attributes[index_attribute][index] is False and results[index] == 'nl':
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
                                              (count_false_en + count_false_nl) / (results_nl + results_nl)) * entropy(
                        count_false_en / (count_false_nl + count_false_en))
                elif count_false_en == 0:
                    rem_false_value = 0
                    # rem_true_value = 0
                    rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * entropy(
                        count_true_en / (count_true_nl + count_true_en))
                else:
                    rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * entropy(
                        count_true_en / (count_true_nl + count_true_en))

                    rem_false_value = (
                                              (count_false_en + count_false_nl) / (results_nl + results_en)) * entropy(
                        count_false_en / (count_false_nl + count_false_en))

                # Find the gain for each attribute
                gain_for_attribute = entropy(results_en / (results_en + results_nl)) - (rem_true_value +
                                                                                        rem_false_value)
                gain.append(gain_for_attribute)
        # Check if the max gain is 0 then return back as no more gain possible along this path
        continue_var = check_for_0_gain(gain)
        if continue_var is False:
            root.value = prevprediction
            print(root.value)
            return

        # Select the max gain attribute
        max_gain_attribute = gain.index(max(gain))

        seen.append(max_gain_attribute)

        index_True = []
        index_False = []

        # Separate out true and false portion for the found out max gain attribute
        for index in total_results:
            if attributes[max_gain_attribute][index] is True:
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
        root.value = max_gain_attribute

        # Make left portion for the max gain attribute

        left_obj = tree(attributes, None, results, index_True, depth + 1,
                        prediction_at_this_stage, bool_true)
        # Make right portion for the max gain attribute

        right_obj = tree(attributes, None, results, index_False, depth + 1,
                         prediction_at_this_stage, bool_false)
        root.left = left_obj
        root.right = right_obj
        # Recurse left and right portions
        train_decision_tree(left_obj, attributes, seen, results, index_True, depth + 1, prediction_at_this_stage)
        train_decision_tree(right_obj, attributes, seen, results, index_False, depth + 1, prediction_at_this_stage)

        del seen[-1]
