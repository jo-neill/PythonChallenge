### The following script breaks down our refined data source into training and testing data and 
### then trains a linear regression model to predict the relevance_score of future projects. The 
### reason I have chosen to use this model is that it is ideal for predicting a single dependent 
### variable based on one or many independent variables. In our case, we are primarily using the
### size of projects (in ft^2) to predict how relevant the project is to our client. If we were to
### identify more columns that help predict relevance we could easily transform our code below to use
### a multiple linear regression technique instead of using the square footage as the sole predictor.
###
### NOTE: It is important to run the DataSetup.py file first to set up the dataset. This file takes
### care of all CSV augmentation needed before getting into the training of our model.
###
### @Author: Joe O'Neill
import DataSetup
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model

# Initialize the dataset by breaking it into training and testing data
def init_data(input_file):
    # Open the CSV with the updated data set
    data = pd.read_csv(input_file)

    # Identify relevance_score as the label
    y = data[['relevance_score']]
    X = data[['OBJECTID']]

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2)
    return X_train, y_train

# Create a linear regression model and fit it with the training data
def train_model(X_train, y_train):
    regression_model = linear_model.LinearRegression()
    regression_model.fit(X_train, y_train)
    return regression_model

# Test the prediction of a relevance_score
def test_model(model):
    test_project_size = 150000
    print (f'Predicted Relevance Score for {test_project_size}: \n', model.predict([[test_project_size]]))

def main():
    DataSetup.main()
    DataSetup.set_directory('../')
    X_train, y_train = init_data('data/complete_data.csv')
    model = train_model(X_train, y_train)
    test_model(model)

# Execute main on initialization
if __name__ == '__main__':
    main()
