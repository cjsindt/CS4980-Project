import pandas as pd
import matplotlib.pyplot as plt


def read_data():
    global casedata
    casedata = pd.read_csv('./data/Hepatitis B, perinatal infection to Hepatitis C, acute.csv')


# Given a list of years, generate a plot of Hepatitis C (viral, acute), Confirmed cases over those years
# Save the figure in /plots/hepatitis_cases_<years>.png
def plot_cases(years=[2019, 2020, 2021, 2022]):
    cases = casedata.query(f'{" | ".join([f"YEAR == {y}" for y in years])}')
    cases = cases[['YEAR', 'WEEK', 'Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max']].replace('X', 0).astype(float).groupby(['YEAR', 'WEEK'], as_index=False).mean()
    print(cases)
    plt.plot(range(len(cases)), cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'], 'r', label='Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max')
    # shade the hepatitis seasons
    plt.fill([0, 20, 20, 0], [0, 0, max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max']), max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'])], 'b', alpha=0.2, label='Flu Season')
    for i in range(len(years)-1):
        plt.fill([(40) + (52*i), (40) + (32) + (52*i), (40) + (32) + (52*i), (40) + (52*i)], [0, 0, max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max']), max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'])], 'b', alpha=0.2)
    plt.fill([len(cases)-20, len(cases), len(cases), len(cases)-20], [0, 0, max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max']), max(cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'])], 'b', alpha=0.2)
    plt.legend()
    plt.savefig(f'./plots/hepatitis_cases_{"-".join([str(y) for y in years])}')


# takes a list of years and an optional state to calcluate the peaks from the given years flu seasons
# returns a list of tuples where the first element in the tuple is the peak %Unweighted ILI and the second element is the epiweek in which it occured
# the index of each tuple corresponds to its year in the input list
def get_peaks(years=[2019, 2020, 2021, 2022], state=''):
    peaks = []
    for y in years:
        if len(state) == 0:
            cases = casedata.query(f'(YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)')
            cases = aggregate_cases(cases)
        else:
            cases = casedata.query(f'((YEAR == {y-1} & WEEK >= 40) | (YEAR == {y} & WEEK <= 20)) & REGION == \"{state}\"')
            cases = aggregate_cases(cases)

        peak = cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'].max()
        peaks.append((peak, float(cases[cases['Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max'] == peak]['WEEK'].to_string(index=False))))
    return peaks
    

# given a list of peaks and their epiweeks, average each to figure out the average and range of peaks and the average and range of epiweeks in which they occur
# generates box plots for each
def avg_peaks(peaks):
    ili = [t[0] for t in peaks]
    epiweeks = [t[1] for t in peaks]
    print(f'Hepatits C:\n\tmin: {min(ili)}\n\tmax: {max(ili)}\n\tavg: {sum(ili)/len(ili)}')
    print(f'Epiweeks:\n\tmin: {min(epiweeks)}\n\tmax: {max(epiweeks)}\n\tavg: {sum(epiweeks)/len(epiweeks)}')
    plt.boxplot(ili, vert=False)
    plt.show()
    plt.clf()
    plt.boxplot(epiweeks, vert=False)
    plt.show()


# helper function for avg_peak()
# takes case data from query in avg_peak and aggregates it into epiweeks
# if there are multiple regions specified, averages over all regions
def aggregate_cases(cases):
    func = lambda x: x + 12 if x <= 20 else x - 40
    cases = cases[['WEEK', 'Hepatitis C (viral, acute), Confirmed, Previous 52 weeks Max']].replace('X', 0).astype(float).groupby(['WEEK'], as_index=False).mean()
    cases['WEEK'] = cases['WEEK'].apply(func)
    cases = cases.sort_values(by=['WEEK'])
    return cases


if __name__ == '__main__':
    read_data()
    years = list(range(2011,2023))

    #print(get_peaks(years=years[:-3], state='New York'))
    #avg_peaks(get_peaks(years=years[:-3]))

    plot_cases(years[:-3])
