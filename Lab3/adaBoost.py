import math
from treeNode import *
from checkFeatures import *
import pickle


def entropy(value):
        """
        Entropy function
        :param value:Input value
        :return:Calculate entropy and return
        """
        if value == 1:
            return 0
        return (-1) * (value * math.log(value, 2.0) + (1 - value) * math.log((1 - value), 2.0))


def gather_data(file):
        """
        Gathers data from the train.dat file for training
        :param file:input training file
        :return:list of statements and final predictions
        """

        # Open file
        file_details = open(file, encoding="utf-8-sig")
        all_details = ''
        for file_lines in file_details:
            all_details += file_lines

        # Get all the statements
        statements = all_details.split('|')
        all_data_stripped_space = all_details.split()

        for index in range(len(statements)):
            if index < 1:
                continue
            statements[index] = statements[index][:-4]
        statements = statements[1:]

        # Get all the results

        results = []
        pointer = 0
        for values in all_data_stripped_space:
            if values.startswith('nl|') or values.startswith('en|'):
                results.insert(pointer, values[0:2])
                pointer = pointer + 1

        return statements, results


def collect_data_ada(example_file, hypothesis_file):
    """
    Collection of data for Adaboost , collection of stumps formed
    :param example_file:Training file for training
    :param hypothesis_file:Hypothesis file to write the set of hypothesis
    :return:None
    """
    # Collection of examples from the training file
    statements, results = gather_data(example_file)
    weights = [1 / len(statements)] * len(statements)

    # Number of hypothesis
    number_of_decision_stumps = 50

    attribute1 = []
    attribute2 = []
    attribute3 = []
    attribute4 = []
    attribute5 = []
    attribute6 = []
    attribute7 = []
    attribute8 = []
    attribute9 = []
    attribute10 = []
    attribute11 = []

    # For each 15-word line in training set decide on the value of features
    for line in statements:
        attribute1.append(containsQ(line))
        attribute2.append(containsX(line))
        attribute3.append(check_avg_word_length_greater_than_5(line))
        attribute4.append(presence_of_van(line))
        attribute5.append(presence_of_de_het(line))
        attribute6.append(check_for_een(line))
        attribute7.append(check_for_en(line))
        attribute8.append(check_for_common_dutch_words(line))
        attribute9.append(check_for_common_english_words(line))
        attribute10.append(presence_of_a_an_the(line))
        attribute11.append(check_presence_of_and(line))

    attributes = [attribute1, attribute2, attribute3, attribute4, attribute5, attribute6, attribute7, attribute8,
                  attribute9, attribute10, attribute11]

    number_lst = []
    stump_values = []

    hypot_weights = [1] * number_of_decision_stumps

    # Set contining indices of all the examples
    for i in range(len(results)):
        number_lst.append(i)

    # Initialization of the root

    # Adaboost algorithm for training
    for hypothesis in range(0, number_of_decision_stumps):

        root = tree(attributes, None, results, number_lst, 0, None, None)
        # For every hypothesis index generate a hypotesis to be added
        stump = return_stump(0, root, attributes, results, number_lst, weights)
        error = 0
        correct = 0
        incorrect = 0
        for index in range(len(statements)):

            # Check for number of examples that do not match with hypothesis output value and update error value
            if prediction(stump, statements[index], attributes, index) != results[index]:
                error = error + weights[index]
                incorrect = incorrect + 1

        for index in range(len(statements)):

            # Check for number of examples that do mathc with the hypothesis output value and update weights of examples
            if prediction(stump, statements[index], attributes, index) == results[index]:
                weights[index] = weights[index] * error / (1 - error)
                correct = correct + 1
        total = 0
        # Calculation for normalization
        for weight in weights:
            total += weight
        for index in range(len(weights)):
            weights[index] = weights[index] / total

        # Updated values for hypothseis weight
        hypot_weights[hypothesis] = math.log(((1 - error) / (error)), 2)
        stump_values.append(stump)

    # Dump the set of generated hypothesis
    filehandler = open(hypothesis_file, 'wb')
    pickle.dump((stump_values, hypot_weights), filehandler)


def prediction(stump, statement, attributes, index):
    """
    For predicting the stump and the result it will give
    :param stump:Input decision stump
    :param statement:Input statement
    :param attributes:Set of attributes/features we have decided upon
    :param index:Index of the statement that is inputted
    :return:Return final prediction from the stump
    """
    attribute_value = stump.value
    if attributes[attribute_value][index] is True:
        return stump.left.value
    else:
        return stump.right.value


def return_stump(depth, root, attributes, results, total_results, weights):
    """
    Function returns a decision stump
    :param depth:Depth of the tree we are at
    :param root:
    :param attributes:
    :param results:
    :param total_results:
    :param weights:
    :return:
    """
    gain = []
    results_en = 0
    results_nl = 0
    for index in total_results:
        if results[index] == 'en':
            results_en = results_en + 1 * weights[index]
        else:
            results_nl = results_nl + 1 * weights[index]

    for index_attribute in range(len(attributes)):
        count_true_en = 0
        count_true_nl = 0
        count_false_en = 0
        count_false_nl = 0
        for index in total_results:
            if attributes[index_attribute][index] is True and results[index] == 'en':
                count_true_en = count_true_en + 1 * weights[index]
            elif attributes[index_attribute][index] is True and results[index] == 'nl':
                count_true_nl = count_true_nl + 1 * weights[index]
            elif attributes[index_attribute][index] is False and results[index] == 'en':
                count_false_en = count_false_en + 1 * weights[index]
            elif attributes[index_attribute][index] is False and results[index] == 'nl':
                count_false_nl = count_false_nl + 1 * weights[index]

        # Handliing certain outlier conditions
        if count_true_en == 0:
            rem_true_value = 0
            rem_false_value = ((count_false_en + count_false_nl) / (results_nl + results_nl)) * entropy(
                count_false_en / (count_false_nl + count_false_en))
        elif count_false_en == 0:
            rem_false_value = 0
            rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * entropy(
                count_true_en / (count_true_nl + count_true_en))
        else:
            rem_true_value = ((count_true_en + count_true_nl) / (results_nl + results_en)) * entropy(
                count_true_en / (count_true_nl + count_true_en))

            rem_false_value = ((count_false_en + count_false_nl) / (results_nl + results_en)) * entropy(
                count_false_en / (count_false_nl + count_false_en))

        gain_for_attribute = entropy(results_en / (results_en + results_nl)) - (rem_true_value +
                                                                                     rem_false_value)
        gain.append(gain_for_attribute)

    max_gain_attribute = gain.index(max(gain))
    root.value = max_gain_attribute
    count_max_true_en = 0
    count_max_true_nl = 0
    count_max_false_en = 0
    count_max_false_nl = 0

    for index in range(len(attributes[max_gain_attribute])):
        if attributes[max_gain_attribute][index] is True:
            if results[index] == 'en':
                count_max_true_en = count_max_true_en + 1 * weights[index]
            else:
                count_max_true_nl = count_max_true_nl + 1 * weights[index]
        else:
            if results[index] == 'en':
                count_max_false_en = count_max_false_en + 1 * weights[index]
            else:
                count_max_false_nl = count_max_false_nl + 1 * weights[index]

    left_obj = tree(attributes, None, results, None, depth + 1,
                      None, None)
    right_obj = tree(attributes, None, results, None, depth + 1,
                       None, None)
    if count_max_true_en > count_max_true_nl:
        left_obj.value = 'en'
    else:
        left_obj.value = 'nl'
    if count_max_false_en > count_max_false_nl:
        right_obj.value = 'en'
    else:
        right_obj.value = 'nl'

    root.left = left_obj
    root.right = right_obj

    return root


def predict_ada(hypothesis_file, input_test_file):
    """
    Making the prediction using the saved adaboost model
    :param hypothesis_file:File containing the adaboost model
    :param input_test_file:Test file to be tested
    :return:None
    """
    # Loading model from the file
    object = pickle.load(open(hypothesis_file, 'rb'))
    file_open = open(input_test_file)
    sentence_list = []
    counter = 0
    sentence = ''

    # Take out 15-word lines from the test file
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

    attribute1 = []
    attribute2 = []
    attribute3 = []
    attribute4 = []
    attribute5 = []
    attribute6 = []
    attribute7 = []
    attribute8 = []
    attribute9 = []
    attribute10 = []
    attribute11 = []

    # For every line decide on the value of features
    for line in sentence_list:
        attribute1.append(containsQ(line))
        attribute2.append(containsX(line))
        attribute3.append(check_avg_word_length_greater_than_5(line))
        attribute4.append(presence_of_van(line))
        attribute5.append(presence_of_de_het(line))
        attribute6.append(check_for_een(line))
        attribute7.append(check_for_en(line))
        attribute8.append(check_for_common_dutch_words(line))
        attribute9.append(check_for_common_english_words(line))
        attribute10.append(presence_of_a_an_the(line))
        attribute11.append(check_presence_of_and(line))

    attributes = [attribute1, attribute2, attribute3, attribute4, attribute5, attribute6, attribute7, attribute8,
                  attribute9, attribute10, attribute11]

    statement_pointer = 0
    hypot_weights = object[1]
    hypot_list = object[0]

    # For every 15-word line make a prediction
    for sentence in sentence_list:
        total_summation = 0
        for index in range(len(object[0])):
            total_summation += make_final_prediction(hypot_list[index], sentence, attributes,
                                                          statement_pointer) * hypot_weights[index]

        if total_summation > 0:
            print('en')
        else:
            print('nl')
        statement_pointer += 1


def make_final_prediction(stump, sentence, attributes, index):
    """
    Returns prediction based on the input hypothesis(stump) in consideration
    :param stump:Input hypothesis
    :param sentence:Input sentence
    :param attributes:Total attributes/features we have decided on
    :param index:Index of the input test statement in the test statement list
    :return:
    """
    attribute_value = stump.value
    if attributes[attribute_value][index] is True:
        if stump.left.value == 'en':
            return 1
        else:
            return -1
    else:
        if stump.right.value == 'en':
            return 1
        else:
            return -1

