import pandas as pd
import matplotlib.pyplot as plt

# fills 3 variables (data2020, data2021, data2022) with the raw USA csv data from 2020-2022
def read_data():
    global data2020, data2021, data2022
    data2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    data2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    data2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)


if __name__ == '__main__':
    read_data()
    school_closing = data2020[data2020['Jurisdiction'] == 'NAT_TOTAL']
    #schools = data['C1E_School closing'].astype(float)
    print(len(data2020))
    print(len(school_closing))
    plt.plot(range(len(school_closing)), school_closing['C1E_School closing'])
    plt.xlabel('Day #')
    plt.ylabel('School closing severity')
    plt.show()