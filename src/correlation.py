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


economic = ['E1E_Income support',
            'E2E_Debt/contract relief',
            'E3E_Fiscal measures',
            'E4E_International support']


health_system = ['H1E_Public information campaigns',
                 'H2E_Testing policy',
                 'H3E_Contact tracing',
                 'H4E_Emergency investment in healthcare',
                 'H5E_Investment in vaccines',
                 'H6E_Facial Coverings',
                 'H7E_Vaccination policy',
                 'H8E_Protection of elderly people']


def read_data():
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# takes a string or list of policies, a threshold, and a region (State), and returns a 1 for each policy that meets
# or surpasses the provided threshold within the given region.
def get_policy(policy, thresh=1, region=''):
    data = all_policydata[all_policydata['RegionName'] == region]
    func = lambda x: 1 if x >= thresh else 0

    if isinstance(policy, str):
        return data.reset_index()[policy].astype(float).apply(func)
    
    elif isinstance(policy, list):
        p_list = []
        for e in policy:
            p_list.append(data.reset_index()[e].astype(float).apply(func))
        result = p_list[0]
        for e in p_list[1:]:
            result = result.add(e, fill_value=0)
        return result
    
    else:
        print('Invalid Policy data type')


# Takes a region of interest and a list of years and outputs a list of the weekly % unweighted ILI from the FluView data
def get_cases(region, years=[2020, 2021, 2022]):
    data = casedata.query(f'REGION==\"{region}\" & ({" | ".join([f"YEAR == {y}" for y in years])})')
    data = data.reset_index()['%UNWEIGHTED ILI'].astype(float)
    result = []

    # because case data is by week, spread it out to be by day to match policy data
    for d in range(len(data)):
        for i in range(7):
            result.append(data[d])

    return result


def correlate():
    pass


if __name__ == '__main__':
    read_data()

    t = get_policy(health_system, region='New York')
    g = get_cases('New York')
    b = get_cases('New York', years=[2017,2018,2019])
    plt.plot(range(len(t)), t, label='Policy')
    plt.plot(range(len(g)), g, label='2020-2022')
    plt.plot(range(len(b)), b, label='2017-2019')
    plt.legend()
    plt.show()
