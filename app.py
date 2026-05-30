import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="Data Cleaning & Reporting Automation", layout="wide")

st.title("📊 Data Cleaning & Reporting Automation")
st.write("Upload a CSV file to automatically clean data, generate reports, and visualize insights.")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:

    # Load Data
    df = pd.read_csv(uploaded_file)

    st.subheader("📄 Raw Data")
    st.dataframe(df)

    if st.button("🚀 Clean Data & Generate Report"):

        cleaned_df = df.copy()

        # Remove duplicates
        cleaned_df.drop_duplicates(inplace=True)

        # Fill missing values
        for col in cleaned_df.columns:

            if cleaned_df[col].dtype in ["float64", "int64"]:
                cleaned_df[col].fillna(cleaned_df[col].mean(), inplace=True)

            else:
                mode_value = (
                    cleaned_df[col].mode()[0]
                    if not cleaned_df[col].mode().empty
                    else "Unknown"
                )
                cleaned_df[col].fillna(mode_value, inplace=True)

        st.subheader("✅ Cleaned Data")
        st.dataframe(cleaned_df)

        # Metrics
        st.subheader("📈 Automated Report")

        total_rows = len(cleaned_df)
        total_columns = len(cleaned_df.columns)
        duplicates_removed = len(df) - len(cleaned_df)
        missing_before = df.isnull().sum().sum()
        missing_after = cleaned_df.isnull().sum().sum()

        col1, col2, col3, col4, col5 = st.columns(5)

        col1.metric("Rows", total_rows)
        col2.metric("Columns", total_columns)
        col3.metric("Duplicates Removed", duplicates_removed)
        col4.metric("Missing Before", missing_before)
        col5.metric("Missing After", missing_after)

        st.subheader("📊 Visualizations")

        numeric_cols = cleaned_df.select_dtypes(include=["number"]).columns

        if len(numeric_cols) > 0:

            selected_num = st.selectbox(
                "Select Numeric Column",
                numeric_cols
            )

            fig, ax = plt.subplots()
            cleaned_df[selected_num].hist(ax=ax)
            ax.set_title(f"Distribution of {selected_num}")
            st.pyplot(fig)

        categorical_cols = cleaned_df.select_dtypes(include=["object"]).columns

        if len(categorical_cols) > 0:

            selected_cat = st.selectbox(
                "Select Categorical Column",
                categorical_cols
            )

            fig2, ax2 = plt.subplots()

            cleaned_df[selected_cat].value_counts().head(10).plot(
                kind="bar",
                ax=ax2
            )

            ax2.set_title(f"{selected_cat} Distribution")
            st.pyplot(fig2)

        # Download Cleaned Data
        csv = cleaned_df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Cleaned Data",
            data=csv,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )

else:
    st.info("Please upload a CSV file to begin.")