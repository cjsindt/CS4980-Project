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

# Plots all policies relating to containment and closing for a given state that meet a threshold of at least 1 (According to OxCGRT thresholds)
def containment_closing_1(state):
    data = all_data[all_data['RegionName'] == state]
    threshold = 1
    func = lambda x: 1 if x >= threshold else 0
    #ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some Levels', 'Required Closure for All']
    y1 = data['C1E_School closing'].astype(float).apply(func)
    y2 = data['C2E_Workplace closing'].astype(float).apply(func)
    y3 = data['C3E_Cancel public events'].astype(float).apply(func)
    y4 = data['C4E_Restrictions on gatherings'].astype(float).apply(func)
    y5 = data['C5E_Close public transport'].astype(float).apply(func)
    y6 = data['C6E_Stay at home requirements'].astype(float).apply(func)
    y7 = data['C7E_Restrictions on internal movement'].astype(float).apply(func)
    y8 = data['C8E_International travel controls'].astype(float).apply(func)

    policy_labels = ['School Closing', 'Workplace Closing', 'Cancel Public Events', 'Restrictions on Gatherings', 'Close Public Transport', 'Stay at Home Requirements', 'Restrictions on Internal Movement', 'International Travel Controls']

    start_date = datetime.datetime(2020, 1, 1)
    x_range = [start_date + datetime.timedelta(days=i) for i in range(len(data))]

    plt.figure(figsize=(24,6), dpi=200)
    plt.stackplot(x_range, y1.fillna(0), y2.fillna(0), y3.fillna(0), y4.fillna(0), y5.fillna(0), y6.fillna(0), y7.fillna(0), y8.fillna(0), labels=policy_labels)
    #plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    #plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Date')
    plt.ylabel('# of Catergories of Policies In Place')
    plt.title(f'Containment and Closure Policies of at Least Recommended Status for {state} State')
    #plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.savefig(f'./plots/{state}_containment_closure_1.png')
    plt.show()

# Plots all policies relating to containment and closing for a given state that meet a threshold of at least 2 (According to OxCGRT thresholds)
# If a policy does not have a possible ranking of 2, it is included if it is at its max ranking
def containment_closing_2(state):
    data = all_data[all_data['RegionName'] == state]
    threshold = 2
    func = lambda x: 1 if x >= threshold else 0
    #ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some Levels', 'Required Closure for All']
    y1 = data['C1E_School closing'].astype(float).apply(func)
    y2 = data['C2E_Workplace closing'].astype(float).apply(func)
    y3 = data['C3E_Cancel public events'].astype(float).apply(func)
    y4 = data['C4E_Restrictions on gatherings'].astype(float).apply(func)
    y5 = data['C5E_Close public transport'].astype(float).apply(func)
    y6 = data['C6E_Stay at home requirements'].astype(float).apply(func)
    y7 = data['C7E_Restrictions on internal movement'].astype(float).apply(func)
    y8 = data['C8E_International travel controls'].astype(float).apply(func)

    policy_labels = ['School Closing', 'Workplace Closing', 'Cancel Public Events', 'Restrictions on Gatherings', 'Close Public Transport', 'Stay at Home Requirements', 'Restrictions on Internal Movement', 'International Travel Controls']

    start_date = datetime.datetime(2020, 1, 1)
    x_range = [start_date + datetime.timedelta(days=i) for i in range(len(data))]

    plt.figure(figsize=(24,6), dpi=200)
    plt.stackplot(x_range, y1.fillna(0), y2.fillna(0), y3.fillna(0), y4.fillna(0), y5.fillna(0), y6.fillna(0), y7.fillna(0), y8.fillna(0), labels=policy_labels)
    #plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    #plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Date')
    plt.ylabel('# of Catergories of Policies In Place')
    plt.title(f'Containment and Closure Policies of Partially Required Status for {state} State')
    #plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.savefig(f'./plots/{state}_containment_closure_2.png')
    plt.show()


# Plots all policies relating to containment and closing for a given state that meet a threshold of at least 3 (According to OxCGRT thresholds)
# If a policy does not have a possible ranking of 3, it is included if it is at its max ranking
def containment_closing_3(state):
    data = all_data[all_data['RegionName'] == state]
    threshold = 3
    func = lambda x: 1 if x >= threshold else 0
    func2 = lambda x: 1 if x >= (threshold - 1) else 0 # some data points only have severities up to 2
    #ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some Levels', 'Required Closure for All']
    y1 = data['C1E_School closing'].astype(float).apply(func)
    y2 = data['C2E_Workplace closing'].astype(float).apply(func)
    y3 = data['C3E_Cancel public events'].astype(float).apply(func2)
    y4 = data['C4E_Restrictions on gatherings'].astype(float).apply(func)
    y5 = data['C5E_Close public transport'].astype(float).apply(func2)
    y6 = data['C6E_Stay at home requirements'].astype(float).apply(func)
    y7 = data['C7E_Restrictions on internal movement'].astype(float).apply(func2)
    y8 = data['C8E_International travel controls'].astype(float).apply(func)

    policy_labels = ['School Closing', 'Workplace Closing', 'Cancel Public Events', 'Restrictions on Gatherings', 'Close Public Transport', 'Stay at Home Requirements', 'Restrictions on Internal Movement', 'International Travel Controls']

    start_date = datetime.datetime(2020, 1, 1)
    x_range = [start_date + datetime.timedelta(days=i) for i in range(len(data))]

    plt.figure(figsize=(24,6), dpi=200)
    plt.stackplot(x_range, y1.fillna(0), y2.fillna(0), y3.fillna(0), y4.fillna(0), y5.fillna(0), y6.fillna(0), y7.fillna(0), y8.fillna(0), labels=policy_labels)
    #plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    #plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Date')
    plt.ylabel('# of Catergories of Policies In Place')
    plt.title(f'Containment and Closure Policies of Required Status for {state} State')
    #plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.savefig(f'./plots/{state}_containment_closure_3.png')
    plt.show()



# Plots all policies relating to containment and closing for a given state that meet a threshold of at least 4 (According to OxCGRT thresholds)
# If a policy does not have a possible ranking of 4, it is included if it is at its max ranking
def containment_closing_4(state):
    data = all_data[all_data['RegionName'] == state]
    threshold = 4
    func = lambda x: 1 if x >= threshold else 0
    func2 = lambda x: 1 if x >= (threshold - 2) else 0 # some data points only have severities up to 2
    func3 = lambda x: 1 if x >= (threshold - 1) else 0 # some data points only have severities up to 3
    #ticks = ['No Closure', 'Recommended Closure', 'Required Closure for Some Levels', 'Required Closure for All']
    y1 = data['C1E_School closing'].astype(float).apply(func3)
    y2 = data['C2E_Workplace closing'].astype(float).apply(func3)
    y3 = data['C3E_Cancel public events'].astype(float).apply(func2)
    y4 = data['C4E_Restrictions on gatherings'].astype(float).apply(func)
    y5 = data['C5E_Close public transport'].astype(float).apply(func2)
    y6 = data['C6E_Stay at home requirements'].astype(float).apply(func3)
    y7 = data['C7E_Restrictions on internal movement'].astype(float).apply(func2)
    y8 = data['C8E_International travel controls'].astype(float).apply(func)

    policy_labels = ['School Closing', 'Workplace Closing', 'Cancel Public Events', 'Restrictions on Gatherings', 'Close Public Transport', 'Stay at Home Requirements', 'Restrictions on Internal Movement', 'International Travel Controls']

    start_date = datetime.datetime(2020, 1, 1)
    x_range = [start_date + datetime.timedelta(days=i) for i in range(len(data))]

    plt.figure(figsize=(24,6), dpi=200)
    plt.stackplot(x_range, y1.fillna(0), y2.fillna(0), y3.fillna(0), y4.fillna(0), y5.fillna(0), y6.fillna(0), y7.fillna(0), y8.fillna(0), labels=policy_labels)
    #plt.plot(range(len(school_closing)), school_closing['C1NV_School closing'].astype(float), 'b', label='Non-Vaccinated')
    #plt.plot(range(len(school_closing)), school_closing['C1V_School closing'].astype(float), 'g', label='Vaccinated')
    plt.xlabel('Date')
    plt.ylabel('# of Catergories of Policies In Place')
    plt.title(f'Containment and Closure Policies of Required Status for {state} State')
    #plt.yticks([0,1,2,3], ticks)
    plt.legend()
    plt.savefig(f'./plots/{state}_containment_closure_4.png')
    plt.show()

if __name__ == '__main__':
    read_data()
    containment_closing_1('New York')
    containment_closing_4('New York')

    containment_closing_1('Colorado')
    containment_closing_4('Colorado')
