import sys
from decisionTree import *
from adaBoost import *


def main():
    """
    Main Function
    Training: python3 driver.py train <examples> <hypothesisOut> <learning-type(dt or ada)>
    Testing: python3 driver.py predict <hypothesis> <file> <testing-type(dt or ada)>
    """
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


if __name__ == "__main__":
    main()
