import streamlit as st
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="Instagram Influencer Analytics", layout="wide")

# Load CSV directly
df = pd.read_csv("social media influencers - instagram sep-2022.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Convert 'Engagement average' to numeric
df['Engagement average'] = df['Engagement average'].astype(str).str.replace(',', '').astype(float)

# Title
st.title("📊 Instagram Influencer Analytics Dashboard")

# Optional preview
st.subheader("Dataset Preview")
st.dataframe(df.head())

# Prepare top 7 categories
top_7_categories = df['Category_1'].value_counts().nlargest(7).reset_index()
top_7_categories.columns = ['Category', 'Count']

# Create subplot
fig = make_subplots(rows=1, cols=2, 
                    subplot_titles=("Top 10 Influencers by Engagement", "Category Distribution"),
                    specs=[[{"type": "bar"}, {"type": "pie"}]])

categories = df['Category_1'].unique()
countries = df['Audience country'].dropna().unique()

category_bar_indices = {}
category_pie_indices = {}
country_bar_indices = {}
country_pie_indices = {}

# Bar chart traces (category-wise)
bar_traces = []
for idx, cat in enumerate(categories):
    filtered_df = df[df['Category_1'] == cat].nlargest(10, 'Engagement average')
    if not filtered_df.empty:
        bar = px.bar(filtered_df, x='Engagement average', y='Instagram name', color='Category_1',
                     text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'})
        trace = bar.data[0]
        trace.visible = False
        category_bar_indices[cat] = len(bar_traces)
        bar_traces.append(trace)
        fig.add_trace(trace, row=1, col=1)

# Bar chart traces (country-wise)
for idx, country in enumerate(countries):
    filtered_df = df[df['Audience country'] == country].nlargest(10, 'Engagement average')
    if not filtered_df.empty:
        bar = px.bar(filtered_df, x='Engagement average', y='Instagram name', color='Category_1',
                     text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'})
        trace = bar.data[0]
        trace.visible = False
        country_bar_indices[country] = len(bar_traces)
        bar_traces.append(trace)
        fig.add_trace(trace, row=1, col=1)

# Default bar trace
default_bar = px.bar(df.nlargest(10, 'Engagement average'), x='Engagement average', y='Instagram name',
                     color='Category_1', text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'})
default_bar_trace = default_bar.data[0]
default_bar_trace.visible = True
default_bar_index = len(bar_traces)
bar_traces.append(default_bar_trace)
fig.add_trace(default_bar_trace, row=1, col=1)

# Pie chart traces (category-wise)
pie_traces = []
for idx, cat in enumerate(categories):
    filtered_counts = df[df['Category_1'] == cat]['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    if filtered_counts.sum() > 0:
        pie = px.pie(names=top_7_categories['Category'], values=filtered_counts,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        trace = pie.data[0]
        trace.visible = False
        category_pie_indices[cat] = len(pie_traces)
        pie_traces.append(trace)
        fig.add_trace(trace, row=1, col=2)

# Pie chart traces (country-wise)
for idx, country in enumerate(countries):
    filtered_counts = df[df['Audience country'] == country]['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    if filtered_counts.sum() > 0:
        pie = px.pie(names=top_7_categories['Category'], values=filtered_counts,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        trace = pie.data[0]
        trace.visible = False
        country_pie_indices[country] = len(pie_traces)
        pie_traces.append(trace)
        fig.add_trace(trace, row=1, col=2)

# Default pie trace
default_pie = px.pie(top_7_categories, values='Count', names='Category',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
default_pie_trace = default_pie.data[0]
default_pie_trace.visible = True
default_pie_index = len(pie_traces)
pie_traces.append(default_pie_trace)
fig.add_trace(default_pie_trace, row=1, col=2)

# Dropdowns for category
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

# Dropdowns for countries
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

# Layout and styling
fig.update_layout(
    title_text="Instagram Influencer Analytics Dashboard",
    title_x=0.5,
    showlegend=True,
    height=600,
    width=1200,
    template='plotly_white',
    updatemenus=[
        dict(buttons=category_buttons,
             direction="down", showactive=True, x=0.1, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12), bgcolor='rgba(255,255,255,0.8)'),
        dict(buttons=country_buttons,
             direction="down", showactive=True, x=0.5, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12), bgcolor='rgba(255,255,255,0.8)')
    ],
    font=dict(family="Arial", size=12),
    margin=dict(t=150)
)

# Axes labels
fig.update_xaxes(title_text="Engagement (Millions)", row=1, col=1, tickformat=".2s")
fig.update_yaxes(title_text="Influencer", row=1, col=1)

# Show chart in Streamlit
st.plotly_chart(fig, use_container_width=True)
