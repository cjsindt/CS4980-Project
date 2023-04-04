import pandas as pd
import matplotlib.pyplot as plt

# fills 4 variables (data2020, data2021, data2022, all_data) with the raw USA csv data from 2020-2022
def read_data():
    global data2020, data2021, data2022, all_data
    data2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    data2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    data2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_data = pd.concat([data2020, data2021, data2022])

def nat_total_school_closing():
    school_closing = all_data[all_data['Jurisdiction'] == 'NAT_TOTAL']
    ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some', 'Required Closure for All']

    plt.plot(range(len(school_closing)), school_closing['C1E_School closing'].astype(float), 'r', label='Everyone')
    plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Day #')
    plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    read_data()
    nat_total_school_closing()