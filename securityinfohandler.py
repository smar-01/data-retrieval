import pandas as pd

def load_security_info_total(filename):
    """
    Loads security information from a CSV file and returns a dictionary where the keys are security tickers.

    Args:
        filename (str): The path to the CSV file containing security information.

    Returns:
        dict: A dictionary where each key is a ticker, and the value is another dictionary containing
              security details such as 'BBID' and 'Security'.

    Example return structure:
    {
        'AAPL US EQUITY': {
            'BBID': 'AAPL',
            'Security': 'Apple Inc.'
        },
        ...
    }
    """

    df = pd.read_csv(filename)

    security_info_total = {}

    required_columns = ['TICKER', 'BBID', 'Security']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")

    for _, row in df.iterrows():
        ticker = row['TICKER']
        bbid = row['BBID']
        security_description = row['Security']
    
        # If ticker is not already in the dictionary, initialize it with an empty dictionary
        if ticker not in security_info_total:
            security_info_total[ticker] = {}
        
        # Add or update the dictionary for the given ticker
        security_info_total[ticker] = {
            'BBID': bbid,
            'Security': security_description
        }

    return security_info_total