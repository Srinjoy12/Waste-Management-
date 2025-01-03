# -*- coding: utf-8 -*-
"""Infosys Waste Management

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17nW9Iuuh_Noh9JTdvaqzhDLxTi4s44Me
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import scipy.stats as stats
from sklearn.model_selection import train_test_split

from google.colab import files
uploaded = files.upload()

csv_filename = list(uploaded.keys())[0]
df = pd.read_csv(csv_filename)

df

df.isnull().sum()

df.describe()

df.info()

df = df.drop_duplicates()

df['timestamp'] = pd.to_datetime(df['timestamp'])

from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
df['waste_type_encoded'] = label_encoder.fit_transform(df['waste_type'])

from sklearn.preprocessing import StandardScaler
numerical_columns = ['inductive_property', 'capacitive_property', 'moisture_property', 'infrared_property']
scaler = StandardScaler()
df[numerical_columns] = scaler.fit_transform(df[numerical_columns])

df.head()

for feature in numerical_columns:
    plt.figure(figsize=(6, 4))
    sns.histplot(df[feature], kde=True, bins=30)
    plt.title(f'Distribution of {feature}')
    plt.xlabel(feature)
    plt.ylabel('Frequency')
    plt.show()

plt.figure(figsize=(6, 4))
sns.scatterplot(x=df['inductive_property'], y=df['capacitive_property'], hue=df['waste_type'])
plt.title('Scatter Plot of Inductive vs Capacitive Property')
plt.xlabel('Inductive Property')
plt.ylabel('Capacitive Property')
plt.legend(title='Waste Type')
plt.show()

plt.figure(figsize=(6, 4))
sns.boxplot(x=df['waste_type'], y=df['moisture_property'])
plt.title('Box Plot of Moisture Property by Waste Type')
plt.xlabel('Waste Type')
plt.ylabel('Moisture Property')
plt.show()

plt.figure(figsize=(6, 4))
plt.plot(df.index, df['infrared_property'], label='Infrared Property', color='blue')
plt.title('Line Graph of Infrared Property')
plt.xlabel('Index')
plt.ylabel('Infrared Property')
plt.legend()
plt.show()

plt.figure(figsize=(8, 6))
sns.heatmap(df[numerical_columns + ['waste_type_encoded']].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()

X = df[numerical_columns].drop('infrared_property', axis=1)
y = df['infrared_property']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.linear_model import LinearRegression, LogisticRegression

linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

from sklearn.metrics import mean_squared_error, accuracy_score
y_test_binary = y_test.astype(int)
y_pred_linear = linear_model.predict(X_test)
y_pred_class = np.array([1 if pred >= 0.5 else 0 for pred in y_pred_linear])
mse_linear = mean_squared_error(y_test_binary, y_pred_linear)
accuracy_linear = accuracy_score(y_test_binary, y_pred_class)

print("Linear Regression Mean Squared Error:", mse_linear)
print("Linear Regression Accuracy:", accuracy_linear)

df['is_recyclable'] = (df['waste_type_encoded'] == label_encoder.transform(['recyclable'])[0]).astype(int)
X_log = df[numerical_columns]
y_log = df['is_recyclable']

X_train_log, X_test_log, y_train_log, y_test_log = train_test_split(X_log, y_log, test_size=0.2, random_state=42)

logistic_model = LogisticRegression()
logistic_model.fit(X_train_log, y_train_log)

y_pred_log = logistic_model.predict(X_test_log)
accuracy = accuracy_score(y_test_log, y_pred_log)
print("Logistic Regression Accuracy:", accuracy)

def custom_predict(model, input_data):
    prediction = model.predict(input_data)
    return ['Recyclable' if pred == 1 else 'Non-Recyclable' for pred in prediction]

sample_data_linear = pd.DataFrame([[0.5, -0.3, 0.8]], columns=['inductive_property', 'capacitive_property', 'moisture_property'])
sample_data_logistic = pd.DataFrame([[0.5, -0.3, 0.8, 0.9]], columns=['inductive_property', 'capacitive_property', 'moisture_property', 'infrared_property'])

print("Custom Linear Regression Prediction:", custom_predict(linear_model, sample_data_linear))
print("Custom Logistic Regression Prediction:", custom_predict(logistic_model, sample_data_logistic))
print("Logistic Regression Model Accuracy:", accuracy)

from sklearn.ensemble import RandomForestClassifier

df['is_recyclable'] = (df['waste_type_encoded'] == label_encoder.transform(['recyclable'])[0]).astype(int)
X_rf = df[numerical_columns]
y_rf = df['is_recyclable']

X_train_rf, X_test_rf, y_train_rf, y_test_rf = train_test_split(X_rf, y_rf, test_size=0.2, random_state=42)

rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train_rf, y_train_rf)

y_pred_rf = rf_model.predict(X_test_rf)
accuracy_rf = accuracy_score(y_test_rf, y_pred_rf)
print("Random Forest Classifier Accuracy:", accuracy_rf)

from sklearn.model_selection import train_test_split, RandomizedSearchCV

param_dist = {
    'n_estimators': [50, 100, 200, 300],
    'max_depth': [None, 10, 20, 30, 40],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

rf_random = RandomizedSearchCV(estimator=RandomForestClassifier(random_state=42),
                               param_distributions=param_dist,
                               n_iter=50, cv=3, verbose=2, random_state=42, n_jobs=-1)

rf_random.fit(X_train_rf, y_train_rf)

best_rf_model = rf_random.best_estimator_
y_pred_rf = best_rf_model.predict(X_test_rf)
accuracy_rf = accuracy_score(y_test_rf, y_pred_rf)
print("Best Parameters for Random Forest:", rf_random.best_params_)
print("Improved Random Forest Classifier Accuracy:", accuracy_rf)

from sklearn.model_selection import train_test_split, GridSearchCV
param_grid_rf = {
    'n_estimators': [200, 300, 500],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

rf_model = RandomForestClassifier(random_state=42)
grid_search_rf = GridSearchCV(estimator=rf_model, param_grid=param_grid_rf, cv=5, n_jobs=-1, verbose=2)
grid_search_rf.fit(X_train_smote, y_train_smote)

best_rf_model = grid_search_rf.best_estimator_
y_pred_rf = best_rf_model.predict(X_test)
accuracy_rf = accuracy_score(y_test, y_pred_rf)
print("Best Parameters for Random Forest:", grid_search_rf.best_params_)
print("Random Forest Classifier Accuracy:", accuracy_rf)

df['is_recyclable'] = (df['waste_type_encoded'] == label_encoder.transform(['recyclable'])[0]).astype(int)
X = df[numerical_columns]
y = df['is_recyclable']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from imblearn.over_sampling import SMOTE
smote = SMOTE(random_state=42)
X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

from xgboost import XGBClassifier, cv, DMatrix
dtrain = DMatrix(X_train_smote.values, label=y_train_smote.values)
dtest = DMatrix(X_test.values, label=y_test.values)

param_xgb = {
    'objective': 'binary:logistic',
    'max_depth': 5,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'eval_metric': 'logloss',
    'seed': 42
}

cv_results = cv(
    params=param_xgb,
    dtrain=dtrain,
    num_boost_round=200,
    nfold=5,
    metrics='logloss',
    early_stopping_rounds=10,
    as_pandas=True,
    seed=42
)

optimal_boost_rounds = len(cv_results)
xgb_model = XGBClassifier(
    n_estimators=optimal_boost_rounds,
    max_depth=param_xgb['max_depth'],
    learning_rate=param_xgb['learning_rate'],
    subsample=param_xgb['subsample'],
    random_state=42
)

xgb_model.fit(X_train_smote.values, y_train_smote.values)

y_pred_xgb = xgb_model.predict(X_test.values)
accuracy_xgb = accuracy_score(y_test.values, y_pred_xgb)
print("Optimal Boost Rounds for XGBoost:", optimal_boost_rounds)
print("XGBoost Classifier Accuracy:", accuracy_xgb)

from lightgbm import LGBMClassifier

lgb_model = LGBMClassifier(random_state=42)
lgb_model.fit(X_train_smote, y_train_smote)
y_pred_lgb = lgb_model.predict(X_test)
accuracy_lgb = accuracy_score(y_test, y_pred_lgb)
print("LightGBM Classifier Accuracy:", accuracy_lgb)

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

model = Sequential([
    Dense(64, activation='relu', input_dim=X_train_smote.shape[1]),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(X_train_smote, y_train_smote, epochs=50, batch_size=32, validation_split=0.2)

accuracy_nn = model.evaluate(X_test, y_test)[1]
print("Neural Network Accuracy:", accuracy_nn)

import numpy as np

def predict_waste_type(inductive, capacitive, moisture, infrared, scaler, model):
    input_data = np.array([[inductive, capacitive, moisture, infrared]])
    prediction = model.predict(input_data)

    return "Recyclable" if prediction[0][0] > 0.5 else "Non-Recyclable"

inductive = 0.9
capacitive = 0.12
moisture = 0.47
infrared = 16.27


result = predict_waste_type(inductive, capacitive, moisture, infrared, scaler, model)
print("Prediction Result:", result)