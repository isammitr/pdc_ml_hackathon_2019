import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, StratifiedKFold, learning_curve
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
import os


### Predict Petition Category ###
print('Predicting petition category')
# Read data
X_train_path = os.path.join(os.getcwd(), 'data/split/train/X_cat100.csv')
y_train_path = os.path.join(os.getcwd(), 'data/split/train/y_cat100.csv')
X_test_path = os.path.join(os.getcwd(), 'data/split/test/X_cat100.csv')

X_train=pd.read_csv(X_train_path)
y_train=pd.read_csv(y_train_path,header=None)[0]
X_test=pd.read_csv(X_test_path)

# Training Models
# Model hypter-parameter tuning was done separately. Not included in this code
# LogReg performed better than XGBoost as well as Voting. So we used LogReg only to predict petition categories

# 1. Logistic Regression
logreg=LogisticRegression(random_state=51,C=50,class_weight='balanced')
logreg.fit(X_train,y_train)

y_cat_pred_lr=logreg.predict(X_test)

del X_train,y_train

### Predict is_victory ###
# Read data
X_train=pd.read_csv(X_train_path)
y_train=pd.read_csv(y_train_path,header=None)[0]

# Append predicted 'petition_category'
X_test['petition_category']=y_cat_pred_lr

# Label Encoding of petition_category
le=LabelEncoder()
X_train['petition_category']=le.fit_transform(X_train['petition_category'])
X_test['petition_category']=le.transform(X_test['petition_category'])

# Training Models
# Model hypter-parameter tuning was done separately. Not included in this code

print('Predicting petition victory status')

# 1. Logistic Regression
logreg=LogisticRegression(random_state=51,C=20,class_weight='balanced')
logreg.fit(X_train,y_train)
y_pred_lr=logreg.predict(X_test)

#2. XGBoost
xgb_params={'colsample_bylevel': 1, 'colsample_bytree': 1, 'max_depth': 3, 
            'min_child_weight': 50, 'reg_alpha': 0.5, 'reg_lambda': 1, 
            'scale_pos_weight': 5, 'subsample': 0.5}
xgb=XGBClassifier(random_state=51,n_jobs=-1,**xgb_params)
xgb.fit(X_train,y_train)
y_pred_xgb=xgb.predict(X_test)

#3. Ensemble : Voting Classifier with soft voting
vc=VotingClassifier([('xgb',xgb),('logreg',logreg)],voting='soft')
vc.fit(X_train,y_train)
y_pred_vc=vc.predict(X_test)

# Learning Curve
cv=StratifiedKFold(3,random_state=51)
lc=learning_curve(vc,X_train,y_train,cv=cv,scoring='recall',
                  n_jobs=1,random_state=51)
size=lc[0]
train_score=[lc[1][i].mean() for i in range (0,5)]
test_score=[lc[2][i].mean() for i in range (0,5)]
fig=plt.figure(figsize=(10,6))
plt.plot(size,train_score,label='Train')
plt.plot(size,test_score,label="Test")
plt.title('Learning Curve', size=14)
plt.xlabel('Sample Size',size=12)
plt.ylabel('Recall',size=12)
plt.legend()
fig.savefig('data/learning_curve.png',dpi=200)

del X_train, y_train, X_test

### Submitting Results ###
print('Creating submission file')

data_path = os.path.join(os.getcwd(), 'data/validation/validation.json')
data = pd.read_json(data_path)
sub=pd.DataFrame()
sub['petition_id']=data['petition_id']
sub['predicted_petition_category']=y_cat_pred_lr
sub['predicted_petition_is_victory']=y_pred_vc
sub.to_csv('data/submission.csv',index=False)

print('Submission file ready')
