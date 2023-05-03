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
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata, casedatachlam2018, casedatachlam2019, casedatachlam2020, casedatachlam2021, all_chlam
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')
    casedatachlam2018 = pd.read_csv('./data/Chlamydia/Chlamydia 2018.csv')
    casedatachlam2019 = pd.read_csv('./data/Chlamydia/Chlamydia 2019.csv')
    casedatachlam2020 = pd.read_csv('./data/Chlamydia/Chlamydia 2020.csv')
    casedatachlam2021 = pd.read_csv('./data/Chlamydia/Chlamydia 2021.csv')
    chlams = [casedatachlam2018, casedatachlam2019, casedatachlam2020, casedatachlam2021]
    for chlam in chlams:
        chlam.sort_values(["MMWR Week"], axis=0, ascending=[True], inplace=True)
    all_chlam = pd.concat(chlams)


# takes a string or list of policies, a threshold, and a region (State), and returns a 1 for each policy that meets
# or surpasses the provided threshold within the given region.
def get_policy(policy, thresh=1, region=''):
    data = all_policydata[all_policydata['RegionName'] == region]
    func = lambda x: 1 if x >= thresh else 0

    if isinstance(policy, str):
        #print("policy result: ", result)
        return data.reset_index()[policy].astype(float).apply(func)
    
    elif isinstance(policy, list):
        p_list = []
        for e in policy:
            p_list.append(data.reset_index()[e].astype(float).apply(func))
        result = p_list[0]
        for e in p_list[1:]:
            result = result.add(e, fill_value=0)
        #print("policy result: ", result)
        return result
    
    else:
        print('Invalid Policy data type')


# Takes a region of interest and a list of years and outputs a list of the weekly % unweighted ILI from the FluView data
def get_cases(region, years=[2020, 2021, 2022]):
    data = casedata.query(f'REGION==\"{region}\" & ({" | ".join([f"YEAR == {y}" for y in years])})')
    d1 = data.reset_index()['%UNWEIGHTED ILI'].astype(float)
    #d2 = data.reset_index()['WEEK'].astype(int)
    result = []

    # because case data is by week, spread it out to be by day to match policy data
    for d in range(len(d1)):
        #print(str(d) + ": " + str(d1[d]) + ", from week: " + str(d2[d]))
        for i in range(7):
            result.append(d1[d])

    return result

def get_chlam(region, years=[2019, 2020, 2021]):
    r = region.upper()
    data = all_chlam.query(f'`Reporting Area`==\"{r}\" & ({" | ".join([f"`MMWR Year` == {y}" for y in years])})')
    #data = all_chlam.query(f'Reporting Area==\"{region}\" & ({" | ".join([f"MMWR Year == {y}" for y in years])})')
    d1 = data.reset_index()['Chlamydia trachomatis infection, Current week'].astype(float)
    #d2 = data.reset_index()['MMWR Week'].astype(int)
    result = []

    # as with ILI cases, spread out to match policy data
    for d in range(len(data)):
        # if # cases is nan, replace with 0
        if(d1[d] != d1[d]):
            d1[d] = 0
        #print(str(d) + ": " + str(d1[d]) + ", from week: " + str(d2[d]))
        
        for i in range(7):
            result.append(d1[d] / 7)

    return result


def correlate():
    pass


if __name__ == '__main__':
    read_data()
    epiweek_start = 40*7
    epi_length = 32

    state = 'New York'

    t = get_policy(containment_closing, region=state)
    t1 = t[:731]
    #print("t slice", t1)
    g = get_cases(state)
    b = get_cases(state, years=[2017,2018,2019])
    c = get_chlam(state)
    plt.figure(figsize=(24,6), dpi=200)
    plt.plot(range(365, 365+len(t1)), t1, label='Total Number of Policies Enacted', color='blue')
    plt.xlabel('Day #')
    plt.ylabel('Total Policies')
    plt.twinx()
    #plt.plot(range(len(g)), g, label='2020-2022 % Unweighted ILI', color='red')
    plt.plot(range(len(c)), c, label='2019-2021 # Chlamydia cases', color='purple')
    #plt.plot(range(len(b)), b, label='2017-2019')
    #plt.fill([0, 20*7, 20*7, 0], [0, 0, max(t), max(t)], 'b', alpha=0.2, label='2019-2020 Flu Season')
    #plt.fill([epiweek_start, epiweek_start + epi_length*7, epiweek_start + epi_length*7, epiweek_start], [0, 0, max(t), max(t)], 'r', alpha=0.2, label='2020-2021 Flu Season')
    #plt.fill([epiweek_start+365, epiweek_start + epi_length*7 + 365, epiweek_start + epi_length*7 + 365, epiweek_start + 365], [0, 0, max(t), max(t)], 'y', alpha=0.2, label='2021-2022 Flu Season')
    #plt.fill([epiweek_start+365*2, 1095, 1095, epiweek_start + 365*2], [0, 0, max(t), max(t)], 'g', alpha=0.2, label='2022-2023 Flu Season')
    plt.title(f'Number of Policies and # Cases for {state} State')
    plt.ylabel('# Cases')
    plt.legend()
    plt.show()
    #plt.savefig(f'./plots/PolicyNumVsCase{state}.png')
