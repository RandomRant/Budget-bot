import pandas as pd
import numpy as np
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from joblib import dump, load


### uncomment block below to train and save new model
#df = pd.read_excel('Financial Tracker - 2.0.xlsm', header=0)
#df=df[df['Date']>'01-01-2020']
#df=df.dropna(subset=['Head','Transaction Description'])
#df=df[['Transaction Description','Head']]
#df['Head']=df['Head'].apply(lambda x: x.upper())

##Split into training and Validation sets

#X=df['Transaction Description']
#y=df['Head']
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


#text_clf_svm = Pipeline([('vect', CountVectorizer()),
#                         ('clf-svm', SGDClassifier(loss='modified_huber', penalty='l2',
#                               alpha=1e-3, max_iter=1000, random_state=42)),
#                         ])

#text_clf_svm = text_clf_svm.fit(X_train, y_train)
#predicted_svm = text_clf_svm.predict(X_test)
#print(np.mean(predicted_svm == y_test))
#dump(text_clf_svm, 'model.joblib') 

### end of training code

text_clf_svm=load('model.joblib')

df = pd.read_csv('.\\masterETL.csv', header=0)
df=df.dropna(subset=['Transaction Description'])
df = df[df['Head'].isnull()]
df1=df['Transaction Description']
predicted_svm= text_clf_svm.predict(df1)
z=pd.Series(predicted_svm)
df=df.reset_index(drop=True)

df['Head']=z

df.to_csv('masterETL.csv', index=False)