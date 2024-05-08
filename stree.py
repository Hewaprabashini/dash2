import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Superstore", page_icon=":bar_chart:", layout="wide")
st.title("\U0001F4CA Sample Superstore EDA")

f1 = st.file_uploader(':file_folder: Upload a file', type=(["csv", "xlsx"]))
if f1 is not None:
    filename = f1.name
    st.write(filename)
    df = pd.read_csv(filename, encoding="ISO-8859-1")
else:
    df = pd.read_csv("Global_Superstore_lite.csv", encoding="ISO-8859-1")

col1, col2 = st.columns(2)
df["Order Date"] = pd.to_datetime(df["Order Date"])

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter:")

# Create filters for Sub-Category
SubCategory = st.sidebar.multiselect("Pick Sub-Category (Antecedents)", df["Sub-Category"].unique())
SubCategoryDesc = st.sidebar.multiselect("Pick Sub-Category (Descendants)", df["Sub-Category"].unique())
if not SubCategory and not SubCategoryDesc:
    filtered_df = df.copy()
elif not SubCategoryDesc:
    filtered_df = df[df["Sub-Category"].isin(SubCategory)]
elif not SubCategory:
    filtered_df = df[df["Sub-Category"].isin(SubCategoryDesc)]
else:
    filtered_df = df[
        (df["Sub-Category"].isin(SubCategory)) | (df["Sub-Category"].isin(SubCategoryDesc))
    ]

with st.expander("Category_view Data"):
    st.write(
        filtered_df.pivot_table(
            index="Category", columns="Sub-Category", values="Sales", aggfunc="sum"
        ).style.background_gradient(cmap="Blues")
    )

st.subheader("Sales Heatmap")
heatmap_fig = px.imshow(
    filtered_df.pivot_table(
        index="Category", columns="Sub-Category", values="Sales", aggfunc="sum"
    ),
    labels=dict(x="Sub-Category", y="Category", color="Sales"),
    title="Sales Heatmap",
)
st.plotly_chart(heatmap_fig, use_container_width=True)

st.subheader("Month-wise Sub-category Sales Summary")
filtered_df["month"] = filtered_df["Order Date"].dt.strftime("%b")
sub_Category_year = pd.pivot_table(
    data=filtered_df, values="Sales", index=["Sub-Category"], columns="month"
)
st.write(sub_Category_year.style.background_gradient(cmap="Blues"))

# Scatter plot
scatter_fig = px.scatter(filtered_df, x="Sales", y="Profit", size="Quantity")
scatter_fig.update_layout(title="Sales Vs Profit")
st.plotly_chart(scatter_fig, use_container_width=True)

# Download buttons
csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Download Data as CSV",
    data=csv,
    file_name="filtered_data.csv",
    mime="text/csv",
    help="Click here to download the data as a CSV file",
)
