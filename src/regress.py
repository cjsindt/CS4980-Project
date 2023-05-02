from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')


def get_cases(states=[], years=[2020, 2021, 2022]):
    result = []
    if len(states) == 0:
        data = casedata.query(f'({" | ".join([f"YEAR == {y}" for y in years])})')
        data = data[['WEEK', 'YEAR', '%UNWEIGHTED ILI']].replace('X', 0).astype(float).groupby(['YEAR', 'WEEK']).mean()
    else:
        regions = " | ".join([f'REGION == \"{s}\"' for s in states])
        data = casedata.query(f'({regions}) & ({" | ".join([f"YEAR == {y}" for y in years])})')
    
    data = data.reset_index()['%UNWEIGHTED ILI'].astype(float)

    # because case data is by week, spread it out to be by day to match policy data
    for d in range(len(data)):
        for i in range(7):
            result.append(data[d])

    return np.array(result[:1096])


def get_policies(states=[], category=containment_closing):
    if len(states) == 0:
        data = all_policydata.query(f'Jurisdiction == \"NAT_TOTAL\"')
    else:
        data = all_policydata.query(" | ".join([f'RegionName == \"{s}\"' for s in states]))

    policies = data[[c for c in category]].fillna(0).astype(float).to_numpy()

    return policies


# generates a linear regression model for the given data and prints different metrics to test the model
# Calculates R_square, mean of residuals
def lin_reg(X, y, labels=containment_closing):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    # coefficients
    for i in range(len(category)):
        print(f'{labels[i]}: {model.coef_[i]}')

    y_pred = model.predict(X_test)

    # r squared
    r_squared = r2_score(y_test, y_pred)
    print(f'R-Squared score: {r_squared}')

    # mean of residuals
    residuals = y_test-y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))


# generates a ridge regression model for the given data and prints different metrics to evaluate the model
def ridge_reg(X, y, labels=containment_closing):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = Ridge()

    model.fit(X_train, y_train)

    # coefficients
    for i in range(len(category)):
        print(f'{labels[i]}: {model.coef_[i]}')

    
    y_pred = model.predict(X_test)

    # r squared
    r_squared = r2_score(y_test, y_pred)
    print(f'R-Squared score: {r_squared}')
    
    # mean of residuals
    residuals = y_test-y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))


# generates a correlation matrix
def corr_mat(X, y, labels=containment_closing):
    matrix = np.corrcoef(X.T, y)

    corr_coeffs = matrix[:-1, -1]

    # Sort the correlation coefficients in descending order
    sorted_idxs = np.argsort(np.abs(corr_coeffs))[::-1]

    # Print the features and their correlation coefficients
    for i in sorted_idxs:
        print(f'{labels[i]}: {corr_coeffs[i]}')


if __name__ == '__main__':
    read_data()


    states = ['New York']
    category = health_system

    cases = get_cases(states)
    policies = get_policies(states, category=category)

    print(f'State: {states}\nCategory: {category}')

    print('\n------ Linear Regression ------\n')
    lin_reg(policies, cases, labels=category)
    print('\n------ Ridge Regression ------\n')
    ridge_reg(policies, cases, labels=category)
    print('\n------ Correlation Matrix ------\n')
    corr_mat(policies, cases, labels=category)

