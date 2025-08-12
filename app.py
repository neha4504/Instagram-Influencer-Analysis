import streamlit as st
import pandas as pd
import plotly.express as px

# Set Streamlit page config for dark theme
st.set_page_config(page_title="Instagram Influencer Analytics", layout="wide")

# Load dataset
df = pd.read_csv("social media influencers - instagram sep-2022.csv")

# Clean 'Engagement average' column
df['Engagement average'] = (
    df['Engagement average']
    .astype(str)
    .str.replace(',', '', regex=False)
    .str.extract('(\d+\.?\d*)')[0]
    .astype(float)
)
df = df.dropna(subset=['Engagement average'])

# Streamlit App Header
st.markdown(
    "<h1 style='color: #FFD700; text-align: center;'>Instagram Influencer Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

# Sidebar Filters
st.sidebar.markdown("## Filter Influencers", unsafe_allow_html=True)

country = st.sidebar.selectbox("Select Audience Country", sorted(df['Audience country'].dropna().unique()))
category = st.sidebar.selectbox("Select Category", sorted(df['Category_1'].dropna().unique()))

filtered_df = df[
    (df['Audience country'] == country) &
    (df['Category_1'] == category)
]

top_engaged = filtered_df.nlargest(10, 'Engagement average')

# Column layout
col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(
        top_engaged,
        x='Instagram name',
        y='Engagement average',
        color='Engagement average',
        title='Top 10 Influencers by Engagement',
        template='plotly_dark'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        filtered_df,
        names='Category_2',
        title='Category Breakdown (Secondary)',
        template='plotly_dark'
    )
    st.plotly_chart(fig2, use_container_width=True)

# Metrics Section
st.markdown("---")
total_influencers = len(filtered_df)
avg_engagement = round(filtered_df['Engagement average'].mean(), 2)

col3, col4 = st.columns(2)
col3.metric("Influencers in Segment", total_influencers)
col4.metric("Avg Engagement Rate", f"{avg_engagement}")

