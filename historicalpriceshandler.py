from datetime import datetime, timedelta
import securitydataparser

def clean_zeroes(stock_shares):
    """
    Replaces zero prices with the previous valid price for each stock.
    """
    for stock, prices in stock_shares.items():
        # Initialize the previous value to None
        previous_value = None
    
        # Iterate through the dates and values
        for date, value in prices.items():
            if value == 0 and previous_value is not None:
                # If the value is 0, set it to the previous day's value
                prices[date] = previous_value
            else:
                # Update the previous value to the current day's value
                previous_value = value
    
    return stock_shares


def create_date_range(start_date, end_date):
    """
    Assists load_historical_fields in creating exact range of dates
    for all portfolio holdings.
    """
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.strftime('%Y-%m-%d'))#('%m/%d/%Y'))
        current_date += timedelta(days=1)
    return date_range


def find_latest_fx_rate(events):
    """ 
    Out of all events, find latest event and find that fx rate.
    """

    latest_event = max(events, key=lambda e: datetime.strptime(e["event_date"], "%m/%d/%Y %H:%M:%S"))
    fx_rate = latest_event['fx_rate']

    return fx_rate


def load_historical_prices(portfolio,session,field):
    """
    Loads historical price data for all securities in the portfolio, over a date range from the start 
    of the portfolio's history until today. Multiplies prices by the FX rate and fills zero values 
    with the previous day's data.

    Args:
        portfolio (dict): A dictionary of securities and their events, where each event contains a trade date.
        session (Session): A session object for querying historical data.
        field (str): The field to query (e.g., 'PX_LAST').

    Returns:
        dict: A dictionary where keys are stock names and values are dictionaries with dates as keys 
              and historical prices (multiplied by the FX rate) as values.
    """

    stock_shares = {}  
    
    for stock, events in portfolio.items():
        all_dates = set()
        for event in events:
            all_dates.add(event['trade_date'])
    all_dates = sorted(all_dates, key=lambda x: datetime.strptime(x, '%m/%d/%Y')) 
        
    start_date = datetime.strptime(all_dates[0], '%m/%d/%Y')
    end_date = datetime.today()
    # Start to finish of all events, until today
    date_range = create_date_range(start_date, end_date)

    for stock, events in portfolio.items():
        # Initialize the security's share count dictionary
        stock_shares[stock] = {date: 0 for date in date_range}
        data = securitydataparser.load_security_history(session,stock,field,start_date,end_date)
        fx_rate = find_latest_fx_rate(events)

        for item in data: 
            date = item[0]
            px = item[1]*fx_rate
            
            stock_shares[stock][date] = px

    stock_shares_cleaned = clean_zeroes(stock_shares)

    return stock_shares_cleaned