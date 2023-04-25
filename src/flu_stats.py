import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    global casedata
    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# takes a list of years and an optional state to calcluate the average peaks from the given years flu seasons
def avg_peak(years=[2020, 2021, 2022], state=''):
    peaks = []
    for y in years:
        if state == '':
            cases = casedata.query(f'(YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)')
            cases = aggregate_cases(cases)
        else:
            cases = casedata.query(f'((YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)) & REGION == \"{state}\"')
            cases = aggregate_cases(cases)

# helper function for avg_peak()
# takes case data from query in avg_peak and aggregates it into epiweeks
# if there are multiple regions specified, averages over all regions
def aggregate_cases(cases):
    func = lambda x: x + 12 if x <= 20 else x - 40
    cases = cases[['WEEK', '%UNWEIGHTED ILI']].replace('X', 0).astype(float).groupby(['WEEK'], as_index=False).mean()
    cases['WEEK'] = cases['WEEK'].apply(func)
    cases = cases.sort_values(by=['WEEK'])
    return cases


if __name__ == '__main__':
    read_data()

    avg_peak(state='New York')
