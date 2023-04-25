import pandas as pd


def read_data():
    global casedata
    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# takes a list of years and an optional state to calcluate the average peaks from the given years flu seasons
def avg_peak(years=[2020, 2021, 2022], state='')
    peaks = []
    for y in years:
        if state == '':
            cases = casedata.query(f'')
        else:
            cases = casedata.query(f'')


if __name__ == '__main__':
    read_data()

