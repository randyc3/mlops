import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="SuperKart Sales Forecaster", layout="wide")

st.title("🛒 SuperKart Sales Forecasting Service")
st.write("Enter product and store attributes to predict sales revenue, or upload a batch CSV file.")

# Sidebar URL configuration
BACKEND_URL = st.sidebar.text_input(
    "Backend Service URL", 
    value="http://backend:7860"
)

tab1, tab2 = st.tabs(["Single Prediction", "Batch Prediction"])

with tab1:
    st.header("Predict Single Item Sales")
    
    col1, col2 = st.columns(2)
    
    with col1:
        product_weight = st.number_input("Product Weight", min_value=0.1, value=12.5)
        product_sugar = st.selectbox("Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"])
        product_allocated_area = st.number_input("Product Allocated Area Ratio", min_value=0.0, max_value=1.0, value=0.05)
        product_mrp = st.number_input("Product MRP", min_value=1.0, value=150.0)
        product_type = st.selectbox("Product Type", [
            "Fruits and Vegetables", "Snack Foods", "Frozen Foods", "Dairy",
            "Household", "Baking Goods", "Canned", "Health and Hygiene",
            "Meat", "Soft Drinks", "Breads", "Hard Drinks", "Others",
            "Starchy Foods", "Breakfast", "Seafood"
        ])
        
    with col2:
        store_size = st.selectbox("Store Size", ["Medium", "High", "Low", "Small"])
        store_location_city_type = st.selectbox("Store City Type", ["Tier 1", "Tier 2", "Tier 3"])
        store_type = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Departmental Store", "Food Mart"])
        store_age_years = st.number_input("Store Age (Years)", min_value=1, value=15)
        
    if st.button("Forecast Sales", key="single_predict"):
        payload = {
            "Product_Weight": product_weight,
            "Product_Sugar_Content": product_sugar,
            "Product_Allocated_Area": product_allocated_area,
            "Product_MRP": product_mrp,
            "Product_Type": product_type,
            "Store_Size": store_size,
            "Store_Location_City_Type": store_location_city_type,
            "Store_Type": store_type,
            "Store_Age_Years": int(store_age_years)
        }
        
        try:
            res = requests.post(f"{BACKEND_URL}/v1/predict", json=payload)
            if res.status_code == 200:
                pred = res.json()["prediction"]
                st.success(f"Predicted Total Store Revenue: ${pred:,.2f}")
            else:
                st.error(f"Error from backend: {res.text}")
        except Exception as e:
            st.error(f"Could not connect to backend server: {str(e)}")

with tab2:
    st.header("Batch File Sales Forecast")
    st.write("Upload a CSV file containing the features to forecast sales for multiple products simultaneously.")
    
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        if st.button("Run Batch Forecasting", key="batch_predict"):
            files = {'file': uploaded_file.getvalue()}
            try:
                res = requests.post(f"{BACKEND_URL}/v1/predictbatch", files=files)
                if res.status_code == 200:
                    preds = res.json()
                    st.success("Batch Forecasting Finished!")
                    
                    # Display results in structured table
                    df_results = pd.DataFrame(list(preds.items()), columns=["Row Index", "Predicted Sales Value"])
                    st.dataframe(df_results, use_container_width=True)
                else:
                    st.error(f"Error from backend: {res.text}")
            except Exception as e:
                st.error(f"Could not connect to backend server: {str(e)}")
