import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

# Load dataset
df = pd.read_csv("transformed_instagram_influencers.csv")  # Ensure this file is in the same directory

# Prepare top 7 categories
top_7_categories = df['Category_1'].value_counts().nlargest(7).reset_index()
top_7_categories.columns = ['Category', 'Count']

# Initialize subplot
fig = make_subplots(rows=1, cols=2,
                    subplot_titles=("Top 10 Influencers by Engagement", "Category Distribution"),
                    specs=[[{"type": "bar"}, {"type": "pie"}]])

# Get unique categories and countries
categories = df['Category_1'].unique()
countries = df['Audience country'].dropna().unique()

# Track indices
category_bar_indices = {}
category_pie_indices = {}
country_bar_indices = {}
country_pie_indices = {}

# Add bar traces for each category
bar_traces = []
for cat in categories:
    filtered_df = df[df['Category_1'] == cat].nlargest(10, 'Engagement average')
    if not filtered_df.empty:
        bar = px.bar(filtered_df, x='Engagement average', y='Instagram name', color='Category_1',
                     text_auto='.2s', labels={'Engagement average': 'Engagement (Millions)'})
        trace = bar.data[0]
        trace.visible = False
        category_bar_indices[cat] = len(bar_traces)
        bar_traces.append(trace)
        fig.add_trace(trace, row=1, col=1)

# Add bar traces for each country
for country in countries:
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

# Add pie traces for each category
pie_traces = []
for cat in categories:
    filtered_counts = df[df['Category_1'] == cat]['Category_1'].value_counts().reindex(top_7_categories['Category']).fillna(0)
    if filtered_counts.sum() > 0:
        pie = px.pie(names=top_7_categories['Category'], values=filtered_counts,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        trace = pie.data[0]
        trace.visible = False
        category_pie_indices[cat] = len(pie_traces)
        pie_traces.append(trace)
        fig.add_trace(trace, row=1, col=2)

# Add pie traces for each country
for country in countries:
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

# Dropdowns
category_buttons = [
    dict(label="All Categories", method="update", args=[{
        "visible": [i == default_bar_index for i in range(len(bar_traces))] +
                   [i == default_pie_index for i in range(len(pie_traces))]
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
        "visible": [i == default_bar_index for i in range(len(bar_traces))] +
                   [i == default_pie_index for i in range(len(pie_traces))]
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

# Final layout
fig.update_layout(
    title_text="Instagram Influencer Analytics Dashboard",
    title_x=0.5,
    showlegend=True,
    height=600,
    width=1200,
    template='plotly_dark',
    paper_bgcolor='black',
    plot_bgcolor='black',
    font=dict(family="Arial", size=12, color='white'),
    updatemenus=[
        dict(buttons=category_buttons,
             direction="down", showactive=True, x=0.1, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12, color='white'), bgcolor='rgba(50,50,50,0.9)'),
        dict(buttons=country_buttons,
             direction="down", showactive=True, x=0.5, y=1.2, xanchor="left", yanchor="top",
             font=dict(size=12, color='white'), bgcolor='rgba(50,50,50,0.9)')
    ],
    margin=dict(t=150)
)

fig.update_xaxes(title_text="Engagement (Millions)", row=1, col=1, tickformat=".2s")
fig.update_yaxes(title_text="Influencer", row=1, col=1)

# Save to HTML and show
fig.write_html('influencer_dashboard.html')
fig.show()

