from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Lists below are preset policy categories of interest
# Labels can be found on the OxCGRT
containment_closing = ['C1E_School closing',
                       'C2E_Workplace closing',
                       'C3E_Cancel public events',
                       'C4E_Restrictions on gatherings',
                       'C5E_Close public transport',
                       'C6E_Stay at home requirements',
                       'C7E_Restrictions on internal movement',
                       'C8E_International travel controls']

economic = ['E1E_Income support',
            'E2E_Debt/contract relief']

health_system = ['H1E_Public information campaigns',
                 'H2E_Testing policy',
                 'H3E_Contact tracing',
                 'H6E_Facial Coverings',
                 'H7E_Vaccination policy',
                 'H8E_Protection of elderly people']

investment = ['E3E_Fiscal measures',
              'E4E_International support',
              'H4E_Emergency investment in healthcare',
              'H5E_Investment in vaccines']


# reads in all used datasets for global use
def read_data():
    global policydata2020, policydata2021, policydata2022, all_policydata, casedata
    policydata2020 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2020.csv', dtype=str)
    policydata2021 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2021.csv', dtype=str)
    policydata2022 = pd.read_csv('./data/United States/OxCGRT_USA_differentiated_withnotes_2022.csv', dtype=str)
    all_policydata = pd.concat([policydata2020, policydata2021, policydata2022])

    casedata = pd.read_csv('./data/FluView/ILINet.csv')


# returns ILI case data for the given state over the given years
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


# returns the policies for the given state and category
def get_policies(states=[], category=containment_closing):
    if len(states) == 0:
        data = all_policydata.query(f'Jurisdiction == \"NAT_TOTAL\"')
    else:
        data = all_policydata.query(" | ".join([f'RegionName == \"{s}\"' for s in states]))

    policies = data[category].fillna(0).astype(float).to_numpy()

    return policies


# generates a linear regression model for the given data and prints different metrics to test the model
# Calculates R_square, mean of residuals, and MSE
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
    residuals = y_test - y_pred
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
    residuals = y_test - y_pred
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
    residuals = y_test - y_pred
    mean_residuals = np.mean(residuals)
    print("Mean of Residuals {}".format(mean_residuals))

    # MSE
    mse = mean_squared_error(y_pred=y_pred, y_true=y_test)
    print(f'MSE: {mse}')


if __name__ == '__main__':
    read_data()

    states = ['Colorado']
    category = containment_closing

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