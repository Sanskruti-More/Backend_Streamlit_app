import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Advanced Streamlit App", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
        /* Background and text color */
        .stApp {
            background-color: #121212;
            color: white;
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #1e1e1e;
        }

        /* Button Styling */
        .stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 5px;
            padding: 8px 16px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #0056b3;
        }

        /* DataFrame Styling */
        .stDataFrame {
            background-color: #2c2c2c;
            color: white;
            border-radius: 5px;
        }

        /* Titles and headers */
        h1, h2, h3 {
            color: #00c8ff;
        }

    </style>
""", unsafe_allow_html=True)

# App Title
st.title("📊 Advanced Streamlit Data Explorer")
st.markdown("Upload a CSV file to explore and visualize key insights interactively.")

# Sidebar - File Upload
st.sidebar.header("📂 Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type=["csv"])

if uploaded_file:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File Uploaded Successfully!")

    # Convert Date Columns (if available)
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Create Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📜 Data Preview", "📈 Visualizations", "📌 Insights", "⚙️ Filters"])

    # *Tab 1 - Data Preview*
    with tab1:
        st.write("### 🔍 Data Preview")
        st.dataframe(df.head())

        st.write("### ❌ Missing Values")
        st.write(df.isnull().sum())

    # *Tab 2 - Visualizations*
    with tab2:
        st.write("### 📊 Select a Column for Distribution")
        numeric_cols = df.select_dtypes(include=["int", "float"]).columns
        if len(numeric_cols) > 0:
            column = st.selectbox("Choose a Numeric Column", numeric_cols, key="dist_col")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(df[column], bins=20, kde=True, ax=ax)
            ax.set_title(f"Distribution of {column}")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No numeric columns found in the dataset.")

    # *Tab 3 - Insights (Correlation, Categories)*
    with tab3:
        insights_option = st.selectbox("Select an Analysis Type", ["Correlation", "Top Categories"])

        if insights_option == "Correlation":
            st.write("### 🔥 Correlation Heatmap")
            numeric_df = df.select_dtypes(include=["number"])
            if len(numeric_df.columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 8))
                sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
                ax.set_title("Correlation Heatmap")
                st.pyplot(fig)
            else:
                st.warning("⚠️ Not enough numeric data for correlation analysis.")

        if insights_option == "Top Categories":
            st.write("### 🏆 Top Categories")
            categorical_cols = df.select_dtypes(include=["object"]).columns
            if len(categorical_cols) > 0:
                category_col = st.selectbox("Choose a Categorical Column", categorical_cols, key="cat_col")
                st.bar_chart(df[category_col].value_counts())
            else:
                st.warning("⚠️ No categorical columns found in the dataset.")

    # *Tab 4 - Data Filters*
    with tab4:
        st.sidebar.header("🔍 Data Filters")
        columns = st.sidebar.multiselect("Select Columns to Display", df.columns, default=df.columns)
        st.write("### 🛠 Filtered Data Preview")
        st.dataframe(df[columns])

else:
    st.sidebar.warning("⚠️ Please upload a CSV file to continue.")
    st.info("Upload a CSV file to get insights!")