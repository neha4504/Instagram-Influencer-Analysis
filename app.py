import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Title
st.set_page_config(layout="wide")
st.title("Instagram Influencer Analytics Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload the influencer CSV file", type=["csv"])
if uploaded_file is not None:
    df = pd.read_csv("social media influencers - instagram sep-2022.csv")

    # Top 7 categories
    top_7_categories = df['Category_1'].value_counts().nlargest(7).reset_index()
    top_7_categories.columns = ['Category', 'Count']

    categories = df['Category_1'].dropna().unique()
    countries = df['Audience country'].dropna().unique()

    # Sidebar filters
    selected_category = st.sidebar.selectbox("Filter by Category", ["All"] + list(categories))
    selected_country = st.sidebar.selectbox("Filter by Country", ["All"] + list(countries))

    # Filter dataset
    filtered_df = df.copy()
    if selected_category != "All":
        filtered_df = filtered_df[filtered_df['Category_1'] == selected_category]
    if selected_country != "All":
        filtered_df = filtered_df[filtered_df['Audience country'] == selected_country]

    # Bar chart: Top 10 influencers by engagement
    top_engagement = filtered_df.nlargest(10, 'Engagement average')
    bar_fig = px.bar(
        top_engagement,
        x='Engagement average',
        y='Instagram name',
        color='Category_1',
        orientation='h',
        text='Engagement average',
        title="Top 10 Influencers by Engagement"
    )
    bar_fig.update_layout(yaxis={'categoryorder':'total ascending'})

    # Pie chart: Category distribution
    pie_data = filtered_df['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    pie_fig = px.pie(
        names=pie_data.index,
        values=pie_data.values,
        title="Category Distribution",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )

    # Layout: 2 charts side by side
    col1, col2 = st.columns(2)
    col1.plotly_chart(bar_fig, use_container_width=True)
    col2.plotly_chart(pie_fig, use_container_width=True)

else:
    st.warning("Please upload a CSV file to continue.")
