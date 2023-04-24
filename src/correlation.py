import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


def read_data():
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')




def correlate():
    pass

if __name__ == '__main__':
    read_data()

    