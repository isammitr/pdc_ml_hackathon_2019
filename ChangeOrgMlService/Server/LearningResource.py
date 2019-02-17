# Importing the libraries

#Importing global libraries
import numpy as np
import pandas as pd
import json as js
import sklearn as skl

#Importing project libraries



#Conversion of any categorical variables into numeric values    
'''
    #Function Name : Prepare_Model_data
    #Input         : 
             Inputdataset        : The Name of the input dataset containing the information
             Prediction_Variable : Variable Name that is to be predicted
    #Output
             Returns 2 Lists
             List 1 : the list containing dependent variable values converted to numeric
             List 2 : the list of values for the prediction variable
             DependantVar_List
             Prediction_List
             
             
'''
def Prepare_Model_data(InputDataSet,Prediction_Variable):
    #InputDataSet = dataset
    #Prediction_Variable="petition_is_victory"

    from sklearn.preprocessing import LabelEncoder, OneHotEncoder
    labelencoder = LabelEncoder()


    for ColumnName in list(dataset):
        if ColumnName not in (Prediction_Variable):
            ColNameList.append(ColumnName)


    DependantVar_ds = InputDataSet[ColNameList] 
    Prediction_ds = InputDataSet[Prediction_Variable] 

    DependantVar_List = InputDataSet[ColNameList].values 
    Prediction_List = InputDataSet["petition_is_victory"].values 
    counter=0

    for ColumnName in list(DependantVar_ds):
        counter+=1
        if DependantVar_ds[ColumnName].dtype == "object":
            DependantVar_List[:, counter-1] = labelencoder.fit_transform(DependantVar_List[:, counter-1])

    return DependantVar_List, Prediction_List
    
    
 
#Gradient Boost Classifier


def Run_Model(ModelName,fm_DependantVar_List,fm_PredictionVar_List,Predict_DependantVar_List):

    if ModelName == "Gradient Boost Classifier":
        from sklearn.ensemble import GradientBoostingClassifier
        model= GradientBoostingClassifier(learning_rate=0.01,random_state=1)

        model.fit(fm_DependantVar_List, fm_PredictionVar_List)

        '''
        gbc_train=model.score(X_train,y_train)
        print("gbc_train=",gbc_train)

        gbc_test=model.score(X_test,y_test)
        print("gbc_test=",gbc_test)

        accuracies_gboost= cross_val_score(estimator = model, X = X_train, y = y_train, cv = 10) 
        accuracies_gboost_mean=accuracies_gboost.mean()*100
        print("Accuracy Gradient Boost=",accuracies_gboost_mean)

        accuracies_gboost_std=accuracies_gboost.std()*100
        print("Standard Deviation Gradient Boost=",accuracies_gboost_std)   
        '''

        Prediction_List = model.predict(Predict_DependantVar_List)
        return Prediction_List
    else:
        print("Please pass a valid Model Name")
    
#Prediction_List = Run_Model("Gradient Boost Classifier",DependantVar_List,Prediction_List,DependantVar_List)   

print("Perdicted : ", Prediction_List)
print("Actual :" ,Prediction_List)


