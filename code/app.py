import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from model_pipeline import load_pipeline, predict_churn
from utils import get_retention_actions
import pandas as pd
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Churn Predictor Pro", 
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {font-size: 4rem; color: #1f77b4; text-align: center; margin-bottom: 2rem;}
    .metric-card {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 1.5rem; border-radius: 15px; text-align: center;}
    .risk-high {background-color: #ff4444; color: white; padding: 1rem; border-radius: 10px;}
    .risk-medium {background-color: #ffaa00; color: white; padding: 1rem; border-radius: 10px;}
    .risk-low {background-color: #00cc44; color: white; padding: 1rem; border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🏦 Churn Predictor Pro</h1>', unsafe_allow_html=True)



# Load model
@st.cache_resource
def init_pipeline():
    return load_pipeline()

pipeline = init_pipeline()

# Main tabs
tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📈 Analytics", "ℹ️ About"])

with tab1:
    # Customer Input
    st.header("👤 Customer Profile")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("**Personal Details**")
        creditscore = st.slider("💳 Credit Score", 300, 850, 650, help="Higher = lower risk")
        age = st.slider("🎂 Age", 18, 80, 42)
        tenure = st.slider("📅 Tenure (Years)", 0, 10, 5)
        
    with col2:
        st.subheader("**Financial Details**")
        balance = st.slider("💰 Account Balance", 0, 250000, 100000)
        salary = st.slider("💼 Est. Salary", 0, 200000, 100000)
        products = st.selectbox("📦 Products", [1, 2, 3, 4])
    
    col3, col4, col5 = st.columns(3)
    with col3: geo = st.selectbox("🌍 Geography", ['France', 'Spain', 'Germany'])
    with col4: gender = st.selectbox("⚤ Gender", ['Male', 'Female'])
    with col5: active = st.selectbox("✅ Active?", ['Yes', 'No'])
    
    col6, col7 = st.columns(2)
    with col6: card = st.selectbox("💳 Credit Card?", ['Yes', 'No'])
    
    # Predict Button
    if st.button("🚀 **ANALYZE CHURN RISK**", type="primary", use_container_width=True):
        customer_data = {
            'CreditScore': creditscore, 'Geography': geo, 'Gender': gender,
            'Age': age, 'Tenure': tenure, 'Balance': balance,
            'NumOfProducts': products, 'HasCrCard': 1 if card=='Yes' else 0,
            'IsActiveMember': 1 if active=='Yes' else 0, 'EstimatedSalary': salary
        }
        
        with st.spinner("Analyzing customer risk..."):
            churn_prob = predict_churn(customer_data, pipeline)
        
        # Results Section
        col_a, col_b = st.columns([1,2])
        with col_a:
            st.metric("Churn Probability", f"{churn_prob:.1%}")
            
            risk_class = "HIGH" if churn_prob > 0.6 else "MEDIUM" if churn_prob > 0.4 else "LOW"
            risk_color = "risk-high" if churn_prob > 0.6 else "risk-medium" if churn_prob > 0.4 else "risk-low"
            st.markdown(f'<div class="{risk_color}">**{risk_class} RISK**</div>', unsafe_allow_html=True)
        
        with col_b:
            # Risk Gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number+delta",
                value = churn_prob,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Churn Risk"},
                delta={'reference': 0.5},
                gauge = {
                    'axis': {'range': [None, 1]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 0.4], 'color': "lightgreen"},
                        {'range': [0.4, 0.6], 'color': "yellow"},
                        {'range': [0.6, 1], 'color': "red"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': churn_prob
                    }
                }
            ))
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.subheader("🎯 Retention Strategy")
        actions = get_retention_actions(churn_prob)
        for action in actions:
            st.write(f"• {action}")

with tab2:
    st.header("📈 Model Analytics")
    st.info("Coming soon: Feature importance, prediction history, business ROI")

with tab3:
    st.header("ℹ️ Technical Details")
    st.markdown("""
    **Model Architecture:** ANN (64-32-16-1)
    
    **Key Improvements:**
    • Fixed 3.6% age outliers → +3% ROC-AUC
    • NaN handling → +6% accuracy boost  
    • 3 engineered features → Better patterns
    
    **Performance:**
    | Metric     | Score  | Industry Rank |
    |------------|--------|---------------|
    | ROC-AUC    | 81.72% | Top 15%       |
    | Accuracy   | 84.25% | Top 10%       |
    | Recall     | 75%+   | Business Win  |
    """)

