import pandas as pd

def load_portfolio_tickets_total(filename, limit=None):
    """
    Loads portfolio data from a PTD CSV file and converts it into a portfolio dictionary.

    Args:
        filename (str): The path to the PTD CSV file.
        limit (int, optional): A limit on the number of rows to process from the file. If None, all rows will be processed.

    Returns:
        dict: A dictionary where the keys are security tickers, and the values are lists of event dictionaries.
              Each event contains details like event date, trade amount, new amount, trade price, etc.

    Example structure of the return dictionary:
    {
        'AAPL US EQUITY': [
            {
                'event_date': '05/1/2024',
                'trade_date': '05/1/2024',
                'event_type': 'SELL',
                'trade_amount': -100000,
                'new_amount': 0,
                'trade_price': 100,
                'sec_currency': 'CAD',
                'total': -1000000
            },
            ...
        ]
    }
    """

    try:
        df = pd.read_csv(filename)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return {}
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return {}
    except pd.errors.ParserError as e:
        print(f"Error parsing the file: {e}")
        return {}

    portfolio_tickets_total = {}

    required_columns = ['TICKER', 'Event Date', 'Trade Date', 'Event Type', 'Trade Amount', 
                    'New Amount', 'Trade Price', 'Sec Currency', 'Fx Rate', 'Total']

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in the CSV: {missing_columns}")

    i = 0

    for _, row in df.iterrows():
        security = row['TICKER']
        fx_rate = row['Fx Rate'] if pd.notna(row['Fx Rate']) else 1.0  # Assuming 1.0 is a safe fallback
        event = {
            'event_date': row['Event Date'],
            'trade_date': row['Trade Date'],
            'event_type': row['Event Type'],
            'trade_amount': row['Trade Amount'], 
            'new_amount': row['New Amount'],        
            'trade_price': row['Trade Price'],
            'sec_currency': row['Sec Currency'],
            'fx_rate': fx_rate,
            'total': row['Total']   
        }
        
        if security not in portfolio_tickets_total:
            portfolio_tickets_total[security] = []
        
        portfolio_tickets_total[security].append(event)

        i += 1

        if limit is not None and i>= (limit):
            break
    
    return portfolio_tickets_total  
        
