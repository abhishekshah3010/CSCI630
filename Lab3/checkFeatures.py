def check_avg_word_length_greater_than_5(statement):
    """
    Check the average word length of the statement
    :param statement: Input statement
    :return: Boolean value representing whether the average word size is greater than 5 or lesser than 5
    """
    words = statement.split()
    total_word_size = 0
    total_words = 0
    for word in words:
        total_word_size = total_word_size + len(word)
        total_words = total_words + 1
    if total_word_size / total_words > 5:
        return True
    else:
        return False


def containsQ(statement):
    """
    Check for occurence of the character Q
    :param statement:Input statement
    :return:Boolean value representing the presence of a character
    """
    if statement.find('Q') < 0 or statement.find('q') < 0:
        return False
    else:
        return True


def containsX(statement):
    """
    Check for occurence of the character Q
    :param statement:Input statement
    :return:Boolean value representing the presence of a character
    """
    if statement.find('x') < 0 or statement.find('X') < 0:
        return False
    else:
        return True


def check_for_en(statement):
    """
    Checking for the presence of the word en in the sentence
    :param statement:Input Statement
    :return:Boolean value representing the presence or absence of the word
    """
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') == 'en':
            return True
    return False


def check_for_common_dutch_words(statement):
    """
    Checking for the presence of common dutch words
    :param statement:Input Statement
    :return:Boolean value representing the presence or absence of the common dutch words
    """
    list = ['naar', 'be', 'ik', 'het', 'voor', 'niet', 'met', 'hij', 'zijn', 'ze', 'wij', 'ze', 'er', 'hun', 'zo',
            'over', 'hem', 'weten'
                           'jouw', 'dan', 'ook', 'onze', 'deze', 'ons', 'meest']
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') in list:
            return True
    return False


def check_for_common_english_words(statement):
    """
    Checking for the presence of common english words
    :param statement: Input statement
    :return: Boolean value representing the presence of common english words
    """
    list = ['to', 'be', 'I', 'it', 'for', 'not', 'with', 'he', 'his', 'they', 'we', 'she', 'there', 'their', 'so',
            'about', 'me',
            'him', 'know', 'your', 'than', 'then', 'also', 'our', 'these', 'us', 'most']
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') in list:
            return True
    return False


def presence_of_van(statement):
    """
    Check if the statement contains the string van
    :param statement:Input statement
    :return:Boolean value representing the presence of the string 'van'
    """
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') == 'van':
            return True
    return False


def presence_of_de_het(statement):
    """
    Check if the statement contains the string de and het
    :param statement:Input statement
    :return:Boolean value representing the presence of the word 'de' or 'het' or both
    """
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') == 'de' or word.lower().replace(',', '') == 'het':
            return True
    return False


def presence_of_a_an_the(statement):
    """
    Check for the presence of articles a an the
    If they are present , chances are statement is in  english language
    :param statement:
    :return: Boolean value reprenting the presence of articles
    """
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') == 'a' or word.lower().replace(',', '') == 'an' or word.lower().replace(',',
                                                                                                                 '') == 'the':
            return True
    return False


def check_for_een(statement):
    """
    Checking for the presence of the word een
    :param statement:Input 15-word statement
    :return:Boolean value representing the presence of the word 'een' in the 15-word sentence
    """
    words = statement.split()
    for word in words:
        if word.lower().replace(',', '') == 'een':
            return True
    return False


def check_presence_of_and(sentence):
    """
    Checking presence of 'and' in the sentence
    :param sentence:Input sentence
    :return:Boolean value representing the presence of 'and'
    """
    words = sentence.split()
    for word in words:
        if word.lower().replace(',', '') == 'and':
            return True
    return False