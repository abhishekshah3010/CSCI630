import sys
from decisionTree import *
from adaBoost import *


def main():
    """
    Main Function
    :return: None
    """
    # Check if right command line arguments given
    try:
        if sys.argv[1] == 'train':
            if sys.argv[4] == 'dt':
                collect_data_dt(sys.argv[2], sys.argv[3])
            else:
                collect_data_ada(sys.argv[2], sys.argv[3])
        elif sys.argv[1] == 'predict':
            if sys.argv[4] == 'dt':
                predict_dt(sys.argv[2], sys.argv[3])
            else:
                predict_ada(sys.argv[2], sys.argv[3])
    except:
        print('Syntax :train <examples> <hypothesisOut> <learning-type>')
        print('or')
        print('Syntax :predict <hypothesis> <file> <testing-type(dt or ada)>')


if __name__ == "__main__":
    main()
