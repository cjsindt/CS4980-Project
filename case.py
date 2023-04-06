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

    ticks = [str(counts.axes[0][i])[:-8] for i in range(len(counts.axes[0])) if i % 26 == 0]
    
    print(counts.axes[0])
    plt.plot(range(len(counts)), counts)
    plt.xticks([26*i for i in range(len(ticks))], ticks, rotation=45)
    plt.xlabel('Date')
    plt.ylabel('# of Cases')
    plt.title('Case Count for New York')
    plt.show()
    