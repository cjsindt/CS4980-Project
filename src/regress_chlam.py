from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score, mean_squared_error
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
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata, casedatachlam2018, casedatachlam2019, casedatachlam2020, casedatachlam2021, all_chlam
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')
    casedatachlam2018 = pd.read_csv('./data/Chlamydia/Chlamydia 2018.csv')
    casedatachlam2019 = pd.read_csv('./data/Chlamydia/Chlamydia 2019.csv')
    casedatachlam2020 = pd.read_csv('./data/Chlamydia/Chlamydia 2020.csv')
    casedatachlam2021 = pd.read_csv('./data/Chlamydia/Chlamydia 2021.csv')
    chlams = [casedatachlam2018, casedatachlam2019, casedatachlam2020, casedatachlam2021]
    for chlam in chlams:
        chlam.sort_values(["MMWR Week"], axis=0, ascending=[True], inplace=True)
    all_chlam = pd.concat(chlams)


def get_cases(states=[], years=[2020, 2021]):
    result = []
    states_upper = []
    for state in states:
        states_upper.append(state.upper())
    if len(states_upper) == 0:
        data = all_chlam.query(f'({" | ".join([f"`MMWR Year` == {y}" for y in years])})')
        data = data[['MMWR Week', 'MMWR Year', 'Chlamydia trachomatis infection, Current week']].astype(float).groupby(["MMWR Year", "MMWR Week"]).mean()
        #print(data)
        #data = data[['MMWR Week', 'MMWR Year', 'Chlamydia trachomatis infection, Current week']].replace('X', 0).astype(float).groupby(['YEAR', 'WEEK']).mean()
    else:
        regions = " | ".join([f'`Reporting Area`==\"{s}\"' for s in states_upper])
        data = all_chlam.query(f'({regions}) & ({" | ".join([f"`MMWR Year` == {y}" for y in years])})')
        
        #print(data)
    
    data = data.reset_index()['Chlamydia trachomatis infection, Current week'].astype(float)
    
    for d in range(len(data)):
                if data[d] != data[d]:
                    data[d] = 0
    print(data)
    # because case data is by week, spread it out to be by day to match policy data
    for d in range(len(data)):
        for i in range(7):
            result.append(data[d] / 7)
    print("len: ", len(result))
    return np.array(result[:731])




def get_policies(states=[], category=containment_closing):
    if len(states) == 0:
        data = all_policydata.query(f'Jurisdiction == \"NAT_TOTAL\"')
    else:
        data = all_policydata.query(" | ".join([f'RegionName == \"{s}\"' for s in states]))

    policies = data[category].fillna(0).astype(float).to_numpy()

    return policies[:731]


# generates a linear regression model for the given data and prints different metrics to test the model
# Calculates R_square, mean of residuals
def lin_reg(X, y, labels=containment_closing):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = LinearRegression()

    model.fit(X_train, y_train)

    # coefficients
    for i in range(len(labels)):
        print(f'{labels[i]}: {model.coef_[i]}')

    y_pred = model.predict(X_test)

    # r squared
    r_squared = r2_score(y_test, y_pred)
    print(f'R-Squared score: {r_squared}')


    # mean of residuals
    residuals = y_test-y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))

    # MSE
    mse = mean_squared_error(y_pred=y_pred, y_true=y_test)
    print(f'MSE: {mse}')


# generates a ridge regression model for the given data and prints different metrics to evaluate the model
def ridge_reg(X, y, labels=containment_closing):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    model = Ridge()

    model.fit(X_train, y_train)

    # coefficients
    for i in range(len(labels)):
        print(f'{labels[i]}: {model.coef_[i]}')

    
    y_pred = model.predict(X_test)

    # r squared
    r_squared = r2_score(y_test, y_pred)
    print(f'R-Squared score: {r_squared}')
    
    # mean of residuals
    residuals = y_test-y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))

    # MSE
    mse = mean_squared_error(y_pred=y_pred, y_true=y_test)
    print(f'MSE: {mse}')


# generates a correlation matrix
def corr_mat(X, y, labels=containment_closing):
    matrix = np.corrcoef(X.T, y)

    corr_coeffs = matrix[:-1, -1]

    # Sort the correlation coefficients in descending order
    sorted_idxs = np.argsort(np.abs(corr_coeffs))[::-1]

    # Print the features and their correlation coefficients
    for i in sorted_idxs:
        print(f'{labels[i]}: {corr_coeffs[i]}')


# generates a polynomial regression model and prints metrics to evaluate the model
# calculates the optimal degree using MSE score
# evaluates the model based on r_square and mean of residuals
def poly_reg(X, y, labels=containment_closing):

    degrees = np.arange(1, 9)

    cv_method = KFold(n_splits=5, shuffle=True, random_state=0)

    scores = []

    for degree in degrees:
        poly_features = PolynomialFeatures(degree=degree)
        X_Poly = poly_features.fit_transform(X)

        model = LinearRegression()
        score = np.mean(cross_val_score(model, X_Poly, y, cv=cv_method, scoring='neg_mean_squared_error'))

        scores.append(-score)

    best_degree = degrees[np.argmin(scores)]

    print(scores)

    print(f'Best Degree: {best_degree}')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    poly = PolynomialFeatures(degree=best_degree)
    
    X_poly_train = poly.fit_transform(X_train)
    X_poly_test = poly.fit_transform(X_test)
    
    model = LinearRegression()

    model.fit(X_poly_train, y_train)

    y_pred = model.predict(X_poly_test)

    # coefficients
    for i in range(len(category)):
        print(f'{labels[i]}: {model.coef_[i]}')

    # r squared
    r_squared = r2_score(y_test, y_pred)
    print(f'R-Squared score: {r_squared}')

    # mean of residuals
    residuals = y_test-y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))

    # MSE
    mse = mean_squared_error(y_pred=y_pred, y_true=y_test)
    print(f'MSE: {mse}')


if __name__ == '__main__':
    read_data()

    # because the chlamydia data is stored differently, to get a national view, leave this states list empty
    # but put ["Total"] in get_cases
    states = []
    category = containment_closing

    # give get_cases states as argument for anything other than national view
    cases = get_cases(states)
    policies = get_policies(states, category=category)

    print(f'State: {states}\nCategory: {category}')

    print('\n------ Linear Regression ------\n')
    lin_reg(policies, cases, labels=category)
    print('\n------ Ridge Regression ------\n')
    ridge_reg(policies, cases, labels=category)
    print('\n------ Polynomial Regression ------\n')
    poly_reg(policies, cases, labels=category)
    print('\n------ Correlation Matrix ------\n')
    corr_mat(policies, cases, labels=category)

