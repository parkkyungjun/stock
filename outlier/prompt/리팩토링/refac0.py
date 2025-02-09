from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb
from tqdm import tqdm


class lightGBM:
    def __init__(self, feature, csv_path, iter):
        self.feature = feature
        self.iter = iter
        self.df = pd.read_csv(csv_path)[self.feature + ['label']]
        """
        현재 df의 feature에 해당 하는 열이 int나 float가 아니면 문제가 발생하고 있어
        이를 해결 하기 위해 df의 feature를 조사 한뒤 만약 int나 float가 아니라면 
        각 열의 unique를 구해서 해당 열을 int로 변환하는 코드 추가해줘 init 하는 곳에서 해당 self.df를
        변환하면 되
        for col in self.feature:
            if self.df[col].dtype == 'object':
                unique_vals = self.df[col].unique()
                mapping = {val: i for i, val in enumerate(unique_vals)}
                self.df[col] = self.df[col].map(mapping)
        """
        for col in self.feature:
            if self.df[col].dtype == 'object':
                unique_vals = self.df[col].unique()
                mapping = {val: i for i, val in enumerate(unique_vals)}
                self.df[col] = self.df[col].map(mapping)
                
    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.df.drop(['label'], axis=1), self.df['label'], test_size=0.2, shuffle=True, random_state=42)
        
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_test = lgb.Dataset(X_test, y_test)
        
        model = lgb.train(
            {'objective': 'regression'}, 
            lgb_train,
            valid_sets=[lgb_test],
            num_boost_round=self.iter,
        )

        # preds = model.predict(lgb_test) # predictor.predict 는 원본 csv 데이터를 입력으로 받음
        preds = model.predict(X_test)
        
        print(np.mean((y_test - preds)**2))
        
    def k_fold(self):
        n_splits = 5
        str_kf = StratifiedKFold(n_splits = n_splits, shuffle=True)

        y = self.df['label']
        X = self.df.drop(['label'], axis=1)

        for i, (train_index, test_index) in tqdm(enumerate(str_kf.split(X, y))):
            X_train, X_valid = X.loc[train_index], X.loc[test_index]
            y_train, y_valid = y.loc[train_index], y.loc[test_index]

            lgb_train = lgb.Dataset(X_train[self.feature], y_train)
            lgb_test = lgb.Dataset(X_valid[self.feature], y_valid)

            model = lgb.train(
                {'objective': 'binary'}, 
                lgb_train,
                valid_sets=[lgb_train, lgb_test],
                num_boost_round=self.iter,
            )

            preds = model.predict(X_valid[self.feature])
            acc = accuracy_score(y_valid, np.where(preds >= 0.5, 1, 0))
            auc = roc_auc_score(y_valid, preds)

            print(f'VALID AUC : {auc} ACC : {acc}\n')
            
            

feature = ['manufacturer','model','vehicle','battery','driving','mileage','warranty','accident','year']
csv_path = 'train.csv'
iter = 100


lgbm = lightGBM(feature, csv_path, iter)
lgbm.train()


'refactoring'
"""
prompt: 나는 머신 러닝관련 ai 대회를 많이 진행하기 때문에 범용적으로 사용하려는 lgbm 클래스를 만들고 있어
내가 아직 주니어 개발자여서 코드에 지저분한데 리팩토링을 진행해줘

규칙은 다음과 같아

1. 변수 이름이 애매모호 한것들을 구체적으로 바꿔줘

2. 불필요한 import를 제거해줘

3. 불필요한 코드를 제거해줘

4. 입력 받은 변수를 사용하지 않는 부분을 사용하도록 고쳐줘




from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.model_selection import StratifiedKFold
import lightgbm as lgb
from tqdm import tqdm

import sys
import os
import math

feature = ['manufacturer','model','vehicle','battery','driving','mileage','warranty','accident','year']
csv_path = 'train.csv'
iter = 100

class Myclass:
    def __init__(self, feature, path, iter):
        self.feature = feature
        self.iter = iter
        self.df = pd.read_csv(csv_path)[self.feature + ['label']]

        for col in self.feature:
            if self.df[col].dtype == 'object':
                unique_vals = self.df[col].unique()
                mapping = {val: i for i, val in enumerate(unique_vals)}
                self.df[col] = self.df[col].map(mapping)
                
    def train(self):
        X_train, X_test, y_train, y_test = train_test_split(self.df.drop(['label'], axis=1), self.df['label'], test_size=0.2, shuffle=True, random_state=42)
        
        lgb_train = lgb.Dataset(X_train, y_train)
        lgb_test = lgb.Dataset(X_test, y_test)
        
        if True:
            model = lgb.train(
                {'objective': 'regression'}, 
                lgb_train,
                valid_sets=[lgb_test],
                num_boost_round=self.iter,
            )

            preds = model.predict(X_test)
            
            print(np.mean((y_test - preds)**2))
        
    def k_fold(self):
        n_splits = 5
        str_kf = StratifiedKFold(n_splits = n_splits, shuffle=True)

        y = self.df['label']
        X = self.df.drop(['label'], axis=1)

        for i, (train_index, test_index) in tqdm(enumerate(str_kf.split(X, y))):
            X_train, X_valid = X.loc[train_index], X.loc[test_index]
            y_train, y_valid = y.loc[train_index], y.loc[test_index]

            lgb_train = lgb.Dataset(X_train[self.feature], y_train)
            lgb_test = lgb.Dataset(X_valid[self.feature], y_valid)
            
            if True:
                model = lgb.train(
                    {'objective': 'regression'}, 
                    lgb_train,
                    valid_sets=[lgb_train, lgb_test],
                    num_boost_round=self.iter,
                )

                preds = model.predict(X_test)
                
                print(np.mean((y_test - preds)**2))
            

lgbm = lightGBM(feature, csv_path, iter)
lgbm.train()

"""