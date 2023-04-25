import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    global casedata
    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# takes a list of years and an optional state to calcluate the peaks from the given years flu seasons
# returns a list of tuples where the first element in the tuple is the peak %Unweighted ILI and the second element is the epiweek in which it occured
# the index of each tuple corresponds to its year in the input list
def get_peaks(years=[2020, 2021, 2022], state=''):
    peaks = []
    for y in years:
        if len(state) == 0:
            cases = casedata.query(f'(YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)')
            cases = aggregate_cases(cases)
        else:
            cases = casedata.query(f'((YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)) & REGION == \"{state}\"')
            cases = aggregate_cases(cases)

        peak = cases['%UNWEIGHTED ILI'].max()
        peaks.append((peak, float(cases[cases['%UNWEIGHTED ILI'] == peak]['WEEK'].to_string(index=False))))
    return peaks
    


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

    print(get_peaks(years=[2015,2016,2017,2018,2019]))
