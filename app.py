import streamlit as st
import pandas as pd
import plotly.express as px

# Set page layout
st.set_page_config(page_title="Instagram Influencer Dashboard", layout="wide")

# Load dataset
df = pd.read_csv("social media influencers - instagram sep-2022.csv")  # Replace with your actual CSV file name

# Clean column names
df.columns = df.columns.str.strip()

# Rename for consistency (optional but helps avoid editing all code)
df.rename(columns={"Subscribers": "Followers"}, inplace=True)

# Title
st.title(" Instagram Influencer Dashboard")

# Sidebar filters
st.sidebar.header("Filter Influencers")

min_followers = int(df["Subscribers"].min())
max_followers = int(df["Subscribers"].max())

followers_range = st.sidebar.slider("Select Follower Range:", min_followers, max_followers, (min_followers, max_followers))

filtered_df = df[(df["Subscribers"] >= followers_range[0]) & (df["Subscribers"] <= followers_range[1])]


# KPI section
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Influencers", len(filtered_df))
col2.metric("Average Engagement", f"{filtered_df['Engagement average'].mean():.2f}")
col3.metric("Avg Authentic Engagement", f"{filtered_df['Authentic engagement'].mean():.2f}")

# Charts
st.subheader(" Engagement vs Followers")

fig1 = px.scatter(
    filtered_df,
    x="Followers",
    y="Engagement average",
    size="Authentic engagement",
    color="Category_1",
    hover_data=["Instagram name", "Name"]
)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Audience Country Distribution")

fig2 = px.histogram(
    filtered_df,
    x="Audience country",
    color="Category_1",
    barmode="group"
)
st.plotly_chart(fig2, use_container_width=True)

# Show filtered data
st.subheader("Filtered Influencer Data")
st.dataframe(filtered_df)



