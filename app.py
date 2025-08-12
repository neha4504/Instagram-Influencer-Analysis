import streamlit as st
import pandas as pd
import plotly.express as px

# Title
st.set_page_config(layout="wide")
st.title("Instagram Influencer Analysis Dashboard")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
min_followers = int(df["Followers"].min())
max_followers = int(df["Followers"].max())
follower_range = st.sidebar.slider("Filter by Followers", min_followers, max_followers, (min_followers, max_followers))

filtered_df = df[(df["Followers"] >= follower_range[0]) & (df["Followers"] <= follower_range[1])]

# Summary Metrics
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Influencers", len(filtered_df))
col2.metric("Avg. Engagement Rate", f"{filtered_df['Engagement Rate (%)'].mean():.2f}%")
col3.metric("Avg. Likes", f"{filtered_df['Likes'].mean():,.0f}")

# Visualizations
st.subheader("Followers vs Likes")
fig1 = px.scatter(filtered_df, x="Followers", y="Likes", hover_data=["Username"], color="Engagement Rate (%)", size="Engagement Rate (%)")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Engagement Rate Distribution")
fig2 = px.histogram(filtered_df, x="Engagement Rate (%)", nbins=30)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Top Influencers by Engagement")
top_df = filtered_df.sort_values("Engagement Rate (%)", ascending=False).head(10)
st.dataframe(top_df[["Username", "Followers", "Engagement Rate (%)"]])
