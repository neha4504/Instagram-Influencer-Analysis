import streamlit as st
import pandas as pd

st.set_page_config(page_title="Instagram Influencer Analytics", layout="wide")

st.title("Instagram Influencer Analytics Dashboard")

# Load default CSV (already in the root of your GitHub repo)
df = pd.read_csv("social media influencers - instagram sep-2022.csv", encoding="ISO-8859-1")
df.columns = df.columns.str.strip()  # Clean extra spaces in column names

# Show dataset preview
st.subheader("Dataset Preview")
st.dataframe(df.head(50), use_container_width=True)

# Example analytics
st.subheader("Basic Insights")

# Clean/convert numeric columns if needed
df["Subscribers"] = pd.to_numeric(df["Subscribers"], errors="coerce")

# Top 10 influencers by subscribers
top_influencers = df.sort_values(by="Subscribers", ascending=False).head(10)
st.write("### Top 10 Influencers by Subscribers")
st.dataframe(top_influencers[["Instagram name", "Name", "Subscribers", "Audience country"]])

# Subscribers distribution
st.write("### Subscriber Distribution")
st.bar_chart(top_influencers.set_index("Instagram name")["Subscribers"])
