import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

def load_pipeline():
    """Load complete model pipeline"""
    try:
        pipeline = joblib.load('churn_model_pipeline.pkl')
        return pipeline
    except:
        raise FileNotFoundError("churn_model_pipeline.pkl not found!")

def preprocess_customer(customer_data, pipeline):
    """Apply same preprocessing as training"""
    df_new = pd.DataFrame([customer_data])
    
    # Feature engineering (exact same as training)
    df_new['BalancePerProduct'] = df_new['Balance'] / (df_new['NumOfProducts'] + 1)
    df_new['AgeGroup'] = pd.cut(df_new['Age'], bins=5, labels=[0,1,2,3,4])
    df_new['InactiveHighBalance'] = ((df_new['IsActiveMember'] == 0) & (df_new['Balance'] > 100000)).astype(int)
    
    # Encode
    df_new['Geography'] = pipeline['le_geo'].transform(df_new['Geography'])
    df_new['Gender'] = df_new['Gender'].map({'Female': 0, 'Male': 1})
    df_new = df_new.fillna(0)
    
    # Select exact features
    X_new = df_new[pipeline['feature_names']].fillna(0)
    X_new_scaled = pipeline['scaler'].transform(X_new)
    
    return X_new_scaled

def predict_churn(customer_data, pipeline):
    """Complete prediction pipeline"""
    X_scaled = preprocess_customer(customer_data, pipeline)
    model = pipeline['model']
    prob = model.predict(X_scaled)[0][0]
    return float(prob)
