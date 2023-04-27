from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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


def get_cases(state = '', years=[2020, 2021, 2022]):
    result = []
    if len(state) == 0:
        data = casedata.query(f'({" | ".join([f"YEAR == {y}" for y in years])})')
        data = data[['WEEK', 'YEAR', '%UNWEIGHTED ILI']].replace('X', 0).astype(float).groupby(['YEAR', 'WEEK']).mean()
    else:
        data = casedata.query(f'REGION==\"{state}\" & ({" | ".join([f"YEAR == {y}" for y in years])})')
    
    data = data.reset_index()['%UNWEIGHTED ILI'].astype(float)

    # because case data is by week, spread it out to be by day to match policy data
    for d in range(len(data)):
        for i in range(7):
            result.append(data[d])

    return np.array(result[:1096])


def get_policies(state = '', years=[2020, 2021, 2022]):
    if len(state) == 0:
        data = all_policydata.query(f'Jurisdiction == \"NAT_TOTAL\"')
    else:
        data = all_policydata[all_policydata['RegionName'] == state]

    policies = data[[c for c in containment_closing]].fillna(0).to_numpy()

    return policies


if __name__ == '__main__':
    read_data()

    state = ''

    print(get_cases(state).shape)
    print(get_policies(state).shape)

    model = LinearRegression()

    model.fit(get_policies(state), get_cases(state))

    for i in range(8):
        print(f'{containment_closing[i]}: {model.coef_[i]}')