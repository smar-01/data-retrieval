import plotly.graph_objects as go
from datetime import datetime
import pandas as pd


def visualize(portfolio):
    # Extract all dates and sort them
    all_dates = set()
    for stock_data in portfolio.values():
        all_dates.update(stock_data.keys())

    all_dates = sorted(all_dates, key=lambda date: datetime.strptime(date, '%m/%d/%Y'))

    # Convert portfolio data to DataFrame
    df = pd.DataFrame(index=all_dates)

    for stock, stock_data in portfolio.items():
        df[stock] = df.index.map(stock_data).fillna(0.0)

    # Reset the index to make 'Date' a column
    df = df.reset_index().rename(columns={'index': 'Date'})

    # Create the Plotly figure
    fig = go.Figure()

    # Add traces for each stock
    for stock in df.columns[1:]:
        fig.add_trace(go.Scatter(x=df['Date'], y=df[stock], mode='lines+markers', name=stock))

    # Update layout
    fig.update_layout(
        title='Portfolio Holdings Over Time',
        xaxis_title='Date',
        yaxis_title='Holdings',
        legend_title='Stock',
        xaxis_tickformat='%m/%d/%Y',
        xaxis=dict(tickangle=-45),
        template='plotly_dark'  # Optional: use a different theme
    )

    # Show the figure
    fig.show()