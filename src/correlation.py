import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


containment_closing = ['C1E_School closing',
                       'C2E_Workplace closing',
                       'C3E_Cancel public events',
                       'C4E_Restrictions on gatherings',
                       'C5E_Close public transport',
                       'C6E_Stay at home requirements',
                       'C7E_Restrictions on internal movement',
                       'C8E_International travel controls']


def read_data():
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# takes a string or list of policies, a threshold, and a region (State), and returns that policy (or group of policies) that meet
# or surpass the provided threshold within the given region.
def get_policy(policy, thresh=1, region=''):
    data = all_policydata[all_policydata['RegionName'] == region]
    func = lambda x: 1 if x >= thresh else 0

    if isinstance(policy, str):
        return data[policy].astype(float).apply(func)
    
    elif isinstance(policy, list):
        p_list = []
        for e in policy:
            p_list.append(data[e].astype(float).apply(func))
        result = p_list[0]
        for e in p_list[1:]:
            result = result.add(e, fill_value=0)
        return result
    
    else:
        print('Invalid Policy data type')


def get_cases():
    pass


def correlate():
    pass


if __name__ == '__main__':
    read_data()

    t = get_policy('C1E_School closing', region='New York')
    plt.plot(range(len(t)), t)
    plt.show()
    