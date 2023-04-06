import pandas as pd
import matplotlib.pyplot as plt
import datetime

def read_data():
    global nyc_case_data
    nyc_case_data = pd.read_csv('./data/Influenza_Laboratory-Confirmed_Cases_By_County__Beginning_2009-10_Season.csv')

if __name__ == '__main__':
    read_data()
    nyc_case_data['Week Ending Date'] = pd.to_datetime(nyc_case_data['Week Ending Date'])
    counts = nyc_case_data.groupby(by='Week Ending Date')['Count'].sum()
    plt.plot(range(len(counts)), counts)
    plt.show()
    
    