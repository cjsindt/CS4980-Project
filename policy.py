import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    school_closing = data[data['Jurisdiction'] == 'NAT_TOTAL']

    #schools = data['C1E_School closing'].astype(float)
    print(len(data))
    print(len(school_closing))
    plt.plot(range(len(school_closing)), school_closing['C1E_School closing'])
    plt.xlabel('Day #')
    plt.ylabel('School closing severity')
    plt.show()