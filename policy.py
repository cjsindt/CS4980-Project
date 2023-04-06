import pandas as pd
import matplotlib.pyplot as plt
import datetime

# fills 4 variables (data2020, data2021, data2022, all_data) with the raw USA csv data from 2020-2022
def read_data():
    global data2020, data2021, data2022, all_data
    data2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    data2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    data2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_data = pd.concat([data2020, data2021, data2022])

def nyc_containment_closing():
    new_york = all_data[all_data['RegionName'] == 'New York']
    #ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some Levels', 'Required Closure for All']

    y1 = new_york['C1E_School closing'].where(new_york['C1E_School closing'].astype(float) < 1, 1).where(new_york['C1E_School closing'].astype(float) > 0, 0).astype(float)
    y2 = new_york['C2E_Workplace closing'].where(new_york['C2E_Workplace closing'].astype(float) < 1, 1).where(new_york['C2E_Workplace closing'].astype(float) > 0, 0).astype(float)
    y3 = new_york['C3E_Cancel public events'].where(new_york['C3E_Cancel public events'].astype(float) < 1, 1).where(new_york['C3E_Cancel public events'].astype(float) > 0, 0).astype(float)
    y4 = new_york['C4E_Restrictions on gatherings'].where(new_york['C4E_Restrictions on gatherings'].astype(float) < 1, 1).where(new_york['C4E_Restrictions on gatherings'].astype(float) > 0, 0).astype(float)
    y5 = new_york['C5E_Close public transport'].where(new_york['C5E_Close public transport'].astype(float) < 1, 1).where(new_york['C5E_Close public transport'].astype(float) > 0, 0).astype(float)
    y6 = new_york['C6E_Stay at home requirements'].where(new_york['C6E_Stay at home requirements'].astype(float) < 1, 1).where(new_york['C6E_Stay at home requirements'].astype(float) > 0, 0).astype(float)
    y7 = new_york['C7E_Restrictions on internal movement'].where(new_york['C7E_Restrictions on internal movement'].astype(float) < 1, 1).where(new_york['C7E_Restrictions on internal movement'].astype(float) > 0, 0).astype(float)
    y8 = new_york['C8E_International travel controls'].where(new_york['C8E_International travel controls'].astype(float) < 1, 1).where(new_york['C8E_International travel controls'].astype(float) > 0, 0).astype(float)
    policy_labels = ['School Closing', 'Workplace Closing', 'Cancel Public Events', 'Restrictions on Gatherings', 'Close Public Transport', 'Stay at Home Requirements', 'Restrictions on Internal Movement', 'International Travel Controls']

    start_date = datetime.datetime(2020, 1, 1)
    x_range = [start_date + datetime.timedelta(days=i) for i in range(len(new_york))]

    plt.stackplot(x_range, y1.fillna(0), y2.fillna(0), y3.fillna(0), y4.fillna(0), y5.fillna(0), y6.fillna(0), y7.fillna(0), y8.fillna(0), labels=policy_labels)
    #plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    #plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Date')
    plt.ylabel('# of Catergories of Policies In Place')
    plt.title('Containment and Closure Policies of at Least Recommended Status for New York State')
    #plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    read_data()
    nyc_containment_closing()
