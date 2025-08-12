# app.py
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Instagram Influencer Dashboard")
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #f0f0f0;
    }
    .css-1v0mbdj, .st-bj, .st-dk, .st-dn {
        background-color: #1e1e1e;
    }
    </style>
""", unsafe_allow_html=True)

try:
    df = pd.read_csv("Processed-dataset/transformed_instagram_influencers.csv")
    df.columns = df.columns.str.strip()
except FileNotFoundError:
    st.error("CSV file not found. Please ensure the path is correct and the file exists.")
    st.stop()

# Prepare top_7_categories
top_7_categories = df['Category_1'].value_counts().nlargest(7).reset_index()
top_7_categories.columns = ['Category', 'Count']

# Initialize subplot
fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("Top 10 Influencers by Engagement", "Category Distribution"),
                    specs=[[{"type": "bar"}, {"type": "pie"}]])

# Get unique categories and countries
categories = df['Category_1'].unique()
countries = df['Audience country'].dropna().unique()

# Track which categories and countries have traces
category_bar_indices = {}
category_pie_indices = {}
country_bar_indices = {}
country_pie_indices = {}

# Add bar traces for each category
bar_traces = []
for idx, cat in enumerate(categories):
    filtered_df = df[df['Category_1'] == cat].nlargest(10, 'Engagement average')
    if not filtered_df.empty:
        bar = px.bar(filtered_df, x='Engagement average', y='Instagram name', color='Category_1',
                     text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'},
                     color_discrete_sequence=px.colors.sequential.Plasma_r)
        trace = bar.data[0]
        trace.visible = False
        category_bar_indices[cat] = len(bar_traces)
        bar_traces.append(trace)
        fig.add_trace(trace, row=1, col=1)

# Add bar traces for each country
for idx, country in enumerate(countries):
    filtered_df = df[df['Audience country'] == country].nlargest(10, 'Engagement average')
    if not filtered_df.empty:
        bar = px.bar(filtered_df, x='Engagement average', y='Instagram name', color='Category_1',
                     text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'},
                     color_discrete_sequence=px.colors.sequential.Plasma_r)
        trace = bar.data[0]
        trace.visible = False
        country_bar_indices[country] = len(bar_traces)
        bar_traces.append(trace)
        fig.add_trace(trace, row=1, col=1)

# Default bar trace
default_bar = px.bar(df.nlargest(10, 'Engagement average'), x='Engagement average', y='Instagram name',
                     color='Category_1', text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'},
                     color_discrete_sequence=px.colors.sequential.Plasma_r)
default_bar_trace = default_bar.data[0]
default_bar_trace.visible = True
default_bar_index = len(bar_traces)
bar_traces.append(default_bar_trace)
fig.add_trace(default_bar_trace, row=1, col=1)

# Add pie traces for each category
pie_traces = []
for idx, cat in enumerate(categories):
    filtered_counts = df[df['Category_1'] == cat]['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    if filtered_counts.sum() > 0:
        pie = px.pie(names=top_7_categories['Category'], values=filtered_counts,
                     color_discrete_sequence=px.colors.sequential.Magma_r)
        trace = pie.data[0]
        trace.visible = False
        category_pie_indices[cat] = len(pie_traces)
        pie_traces.append(trace)
        fig.add_trace(trace, row=1, col=2)

# Add pie traces for each country
for idx, country in enumerate(countries):
    filtered_counts = df[df['Audience country'] == country]['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    if filtered_counts.sum() > 0:
        pie = px.pie(names=top_7_categories['Category'], values=filtered_counts,
                     color_discrete_sequence=px.colors.sequential.Magma_r)
        trace = pie.data[0]
        trace.visible = False
        country_pie_indices[country] = len(pie_traces)
        pie_traces.append(trace)
        fig.add_trace(trace, row=1, col=2)

# Default pie trace
default_pie = px.pie(top_7_categories, values='Count', names='Category',
                     color_discrete_sequence=px.colors.sequential.Magma_r)
default_pie_trace = default_pie.data[0]
default_pie_trace.visible = True
default_pie_index = len(pie_traces)
pie_traces.append(default_pie_trace)
fig.add_trace(default_pie_trace, row=1, col=2)

# Create dropdown menus
category_buttons = [
    dict(label="All Categories", method="update", args=[{
        "visible": [True if i == default_bar_index else False for i in range(len(bar_traces))] +
                   [True if i == default_pie_index else False for i in range(len(pie_traces))]
    }])
]
for cat in categories:
    if cat in category_bar_indices and cat in category_pie_indices:
        visible = [False] * len(bar_traces)
        visible[category_bar_indices[cat]] = True
        pie_visible = [False] * len(pie_traces)
        pie_visible[category_pie_indices[cat]] = True
        category_buttons.append(
            dict(label=cat, method="update", args=[{"visible": visible + pie_visible}])
        )

country_buttons = [
    dict(label="All Countries", method="update", args=[{
        "visible": [True if i == default_bar_index else False for i in range(len(bar_traces))] +
                   [True if i == default_pie_index else False for i in range(len(pie_traces))]
    }])
]
for country in countries:
    if country in country_bar_indices and country in country_pie_indices:
        visible = [False] * len(bar_traces)
        visible[country_bar_indices[country]] = True
        pie_visible = [False] * len(pie_traces)
        pie_visible[country_pie_indices[country]] = True
        country_buttons.append(
            dict(label=country, method="update", args=[{"visible": visible + pie_visible}])
        )

# Update layout
fig.update_layout(
    title_text="Instagram Influencer Analytics Dashboard",
    title_x=0.5,
    showlegend=True,
    height=650,
    width=1400,
    template='plotly_dark',
    paper_bgcolor='#121212',
    plot_bgcolor='#121212',
    updatemenus=[
        dict(buttons=category_buttons,
             direction="down", showactive=True, x=0.1, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12), bgcolor='rgba(30,30,30,0.8)', bordercolor='gray'),
        dict(buttons=country_buttons,
             direction="down", showactive=True, x=0.5, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12), bgcolor='rgba(30,30,30,0.8)', bordercolor='gray')
    ],
    font=dict(family="Arial", size=12, color="#f0f0f0"),
    margin=dict(t=150)
)

# Update axes
fig.update_xaxes(title_text="Engagement (Millions)", row=1, col=1, tickformat=".2s")
fig.update_yaxes(title_text="Influencer", row=1, col=1)

st.plotly_chart(fig, use_container_width=True)
