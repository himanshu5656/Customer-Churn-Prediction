🏦 Customer Churn Prediction (ANN + Streamlit)
Short end-to-end project predicting bank customer churn using an Artificial Neural Network and deploying it with a Streamlit UI.

Tech Stack
Python, NumPy, Pandas, Matplotlib/Seaborn

Scikit-learn (preprocessing, metrics)

TensorFlow / Keras (ANN model)

Joblib (saving pipeline)

Streamlit (web UI)


📂 Project Structure
text
churn-prediction/
├─ data/                     # (optional) raw dataset
├─ notebooks/                # EDA + model experiments
├─ app.py                    # Streamlit UI
├─ model_pipeline.py         # Load & predict functions
├─ utils.py                  # Helper functions (actions, etc.)
├─ config.py                 # Config/constants (thresholds, paths)
├─ churn_model_pipeline.pkl  # Saved model + scaler + metadata
├─ requirements.txt
└─ README.md


How to Run

# 1. Create and activate venv
python -m venv venv. 


venv\Scripts\activate    # Windows for activating
# source venv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run Streamlit app
streamlit run app.py
