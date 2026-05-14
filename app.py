import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="Smart CSV Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# TITLE
# =========================

st.title("📊 Smart CSV Analytics Dashboard")

st.markdown(
    "Upload any CSV file and generate automatic insights, analytics, and visualizations."
)

# =========================
# FILE UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("📊 Dashboard Controls")

st.sidebar.markdown("""
Smart CSV Analytics Dashboard

Upload datasets and automatically generate:
- Insights
- Charts
- Data profiling
- Cleaning reports
""")

st.sidebar.info(
    "Supports CSV datasets for automated analytics."
)

# =========================
# MAIN APP
# =========================

if uploaded_file is not None:

    # =========================
    # LOAD DATA
    # =========================

    with st.spinner("Processing dataset..."):

        df = pd.read_csv(uploaded_file)

    st.success(
        f"Dataset Loaded Successfully ✅ "
        f"({df.shape[0]} rows, {df.shape[1]} columns)"
    )

    # =========================
    # EMPTY DATASET CHECK
    # =========================

    if df.empty:

        st.error("Uploaded dataset is empty.")

        st.stop()

    # =========================
    # SAFE AUTO DATE DETECTION
    # =========================

    for col in df.columns:

        if df[col].dtype == 'object':

            try:
                converted_col = pd.to_datetime(df[col])

                if converted_col.notna().sum() > 0.7 * len(df):

                    df[col] = converted_col

            except:
                pass

    # =========================
    # DATA CLEANING
    # =========================

    st.subheader("🧹 Data Cleaning Summary")

    duplicate_rows = df.duplicated().sum()
    missing_values = df.isnull().sum().sum()

    col1, col2 = st.columns(2)

    col1.metric("Duplicate Rows", duplicate_rows)
    col2.metric("Missing Values", missing_values)

    # Remove duplicates
    df = df.drop_duplicates()

    # Numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns

    # Fill missing numeric values
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())

    st.success("Data cleaned successfully ✅")

    st.divider()

    # =========================
    # DATA PREVIEW
    # =========================

    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.head(20),
        use_container_width=True
    )

    st.divider()

    # =========================
    # DATASET PROFILE
    # =========================

    st.subheader("📋 Dataset Profile")

    memory_usage = df.memory_usage(deep=True).sum() / 1024

    dtype_counts = df.dtypes.value_counts()

    profile_col1, profile_col2, profile_col3 = st.columns(3)

    profile_col1.metric("Rows", df.shape[0])
    profile_col2.metric("Columns", df.shape[1])
    profile_col3.metric("Memory Usage (KB)", f"{memory_usage:.2f}")

    st.markdown("### 📊 Data Types Summary")

    dtype_df = pd.DataFrame({
        "Data Type": dtype_counts.index.astype(str),
        "Count": dtype_counts.values
    })

    st.dataframe(
        dtype_df,
        use_container_width=True
    )

    # Missing values table

    st.markdown("### 🚨 Missing Values by Column")

    missing_df = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum().values,
        "Missing Percentage": (
            df.isnull().sum().values / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing_df,
        use_container_width=True
    )

    st.divider()

    # =========================
    # COLUMN TYPE DETECTION
    # =========================

    st.subheader("🧠 Column Type Detection")

    numeric_columns = df.select_dtypes(
        include=['number']
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=['object', 'category']
    ).columns.tolist()

    datetime_columns = df.select_dtypes(
        include=['datetime64[ns]']
    ).columns.tolist()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔢 Numeric Columns")

        if numeric_columns:
            st.write(numeric_columns)
        else:
            st.write("No numeric columns found.")

    with col2:

        st.markdown("### 🏷 Categorical Columns")

        if categorical_columns:
            st.write(categorical_columns)
        else:
            st.write("No categorical columns found.")

    with col3:

        st.markdown("### 📅 Datetime Columns")

        if datetime_columns:
            st.write(datetime_columns)
        else:
            st.write("No datetime columns found.")

    st.divider()

    # =========================
    # KPI SECTION
    # =========================

    st.subheader("📈 Key Metrics")

    total_rows = df.shape[0]
    total_columns = df.shape[1]
    numeric_column_count = len(numeric_columns)

    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", total_rows)
    col2.metric("Columns", total_columns)
    col3.metric("Numeric Columns", numeric_column_count)

    st.divider()

    # =========================
    # SMART VISUALIZATION ENGINE
    # =========================

    st.subheader("📊 Smart Visualizations")

    # ---------- HISTOGRAM ----------

    if len(numeric_columns) > 0:

        st.markdown("### 🔢 Numeric Distribution")

        selected_numeric = st.selectbox(
            "Select Numeric Column",
            numeric_columns
        )

        fig_hist = px.histogram(
            df,
            x=selected_numeric,
            title=f"Distribution of {selected_numeric}"
        )

        fig_hist.update_layout(height=500)

        st.plotly_chart(fig_hist, use_container_width=True)

    # ---------- BAR CHART ----------

    if len(categorical_columns) > 0 and len(numeric_columns) > 0:

        st.markdown("### 📊 Category vs Numeric Analysis")

        selected_category = st.selectbox(
            "Select Categorical Column",
            categorical_columns
        )

        selected_numeric_bar = st.selectbox(
            "Select Numeric Column for Analysis",
            numeric_columns,
            key="bar_numeric"
        )

        grouped_df = (
            df.groupby(selected_category)[selected_numeric_bar]
            .mean()
            .reset_index()
        )

        fig_bar = px.bar(
            grouped_df,
            x=selected_category,
            y=selected_numeric_bar,
            color=selected_category,
            title=f"{selected_numeric_bar} by {selected_category}"
        )

        fig_bar.update_layout(height=500)

        st.plotly_chart(fig_bar, use_container_width=True)

    # ---------- PIE CHART ----------

    if len(categorical_columns) > 0:

        st.markdown("### 🥧 Category Distribution")

        pie_column = st.selectbox(
            "Select Column for Pie Chart",
            categorical_columns,
            key="pie_chart"
        )

        pie_data = df[pie_column].value_counts().reset_index()

        pie_data.columns = [pie_column, "Count"]

        fig_pie = px.pie(
            pie_data,
            names=pie_column,
            values="Count",
            title=f"Distribution of {pie_column}"
        )

        fig_pie.update_layout(height=500)

        st.plotly_chart(fig_pie, use_container_width=True)

    # ---------- LINE CHART ----------

    if len(datetime_columns) > 0 and len(numeric_columns) > 0:

        st.markdown("### 📈 Time Series Analysis")

        selected_date = st.selectbox(
            "Select Date Column",
            datetime_columns
        )

        selected_numeric_line = st.selectbox(
            "Select Numeric Column",
            numeric_columns,
            key="line_numeric"
        )

        trend_df = (
            df.groupby(selected_date)[selected_numeric_line]
            .sum()
            .reset_index()
        )

        fig_line = px.line(
            trend_df,
            x=selected_date,
            y=selected_numeric_line,
            title=f"{selected_numeric_line} Over Time"
        )

        fig_line.update_layout(height=500)

        st.plotly_chart(fig_line, use_container_width=True)

    st.divider()

    # =========================
    # CORRELATION HEATMAP
    # =========================

    st.subheader("🔥 Correlation Heatmap")

    if len(numeric_columns) >= 2:

        correlation = df[numeric_columns].corr()

        fig_corr = px.imshow(
            correlation,
            text_auto=True,
            aspect="auto",
            title="Correlation Matrix"
        )

        fig_corr.update_layout(height=600)

        st.plotly_chart(fig_corr, use_container_width=True)

    st.divider()

    # =========================
    # SMART AUTO INSIGHTS
    # =========================

    st.subheader("🧠 Smart Insights Engine")

    insights = []

    # ---------- HIGH MEAN COLUMN ----------

    if len(numeric_columns) > 0:

        highest_mean_col = df[numeric_columns].mean().idxmax()

        insights.append(
            f"'{highest_mean_col}' has the highest average values among numeric columns."
        )

    # ---------- DUPLICATES ----------

    if duplicate_rows > 0:

        insights.append(
            f"Dataset contained {duplicate_rows} duplicate rows which were removed."
        )

    # ---------- MISSING VALUES ----------

    missing_percentages = (
        df.isnull().sum() / len(df) * 100
    )

    high_missing = missing_percentages[
        missing_percentages > 30
    ]

    for col, percent in high_missing.items():

        insights.append(
            f"Column '{col}' contains {percent:.1f}% missing values."
        )

    # ---------- OUTLIER DETECTION ----------

    for col in numeric_columns:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        outliers = df[
            (df[col] < q1 - 1.5 * iqr) |
            (df[col] > q3 + 1.5 * iqr)
        ]

        if len(outliers) > 0.1 * len(df):

            insights.append(
                f"Column '{col}' may contain significant outliers."
            )

    # ---------- STRONG CORRELATIONS ----------

    if len(numeric_columns) >= 2:

        corr_matrix = df[numeric_columns].corr()

        for i in range(len(corr_matrix.columns)):

            for j in range(i):

                corr_value = corr_matrix.iloc[i, j]

                if abs(corr_value) > 0.7:

                    insights.append(
                        f"Strong correlation detected between "
                        f"'{corr_matrix.columns[i]}' and "
                        f"'{corr_matrix.columns[j]}'."
                    )

    # ---------- DOMINANT CATEGORY ----------

    if len(categorical_columns) > 0:

        for col in categorical_columns:

            top_value = df[col].value_counts(normalize=True).max()

            if top_value > 0.6:

                dominant = df[col].value_counts().idxmax()

                insights.append(
                    f"'{dominant}' dominates the '{col}' column."
                )

    # ---------- DATE DETECTION ----------

    if len(datetime_columns) > 0:

        insights.append(
            "Date columns were automatically detected for trend analysis."
        )

    # ---------- DISPLAY INSIGHTS ----------

    if len(insights) > 0:

        for insight in insights:
            st.info(insight)

    else:

        st.success("No major issues detected in dataset.")

    st.divider()

    # =========================
    # DOWNLOAD CLEANED DATA
    # =========================

    st.subheader("⬇ Download Cleaned Dataset")

    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name='cleaned_dataset.csv',
        mime='text/csv'
    )

    st.divider()

    # =========================
    # FOOTER
    # =========================

    st.markdown("""
    <center>

    Built with ❤️ using Streamlit, Pandas, and Plotly

    </center>
    """, unsafe_allow_html=True)