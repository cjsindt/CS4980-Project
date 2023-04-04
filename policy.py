import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    data = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    school_closing = data[data['C1E_School closing'].astype(float) > 0]
    print(len(data))
    print(len(school_closing))