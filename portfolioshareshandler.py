from datetime import datetime, timedelta

def create_date_range(start_date, end_date):
    """
    Assists load_portfolio_shares_total in creating exact range (list) of dates
    for all portfolio holdings.
    """
    date_range = []
    current_date = start_date
    while current_date <= end_date:
        date_range.append(current_date.strftime('%m/%d/%Y'))
        current_date += timedelta(days=1)
    return date_range

def load_portfolio_shares_total(portfolio):
    """
    Processes the ticket history dictionary to create a dictionary of historical share holdings.

    Args:
        portfolio (dict): A dictionary where the keys are stock names, and the values are lists of events. 
                          Each event contains an event date and transaction information.

    Returns:
        dict: A dictionary where the keys are stock names, and the values are dictionaries where each 
              key is a date (as a string in 'm/d/Y' format) and the value is the share count on that date.
    """

    # Initialize the output dictionary
    stock_shares  = {}  

    all_dates = set()
    for stock, events in portfolio.items():
        for event in events:
            all_dates.add(event['event_date'])
    all_dates = sorted(all_dates, key=lambda x: datetime.strptime(x, '%m/%d/%Y %H:%M:%S')) 
    
    
    for stock, events in portfolio.items():
        current_shares = 0
        start_date = datetime.strptime(all_dates[0], '%m/%d/%Y %H:%M:%S')
        end_date = datetime.today()
        # Start to finish of all events, until today
        date_range = create_date_range(start_date, end_date)

        # Initialize the security's share count dictionary
        stock_shares[stock] = {date: 0 for date in date_range}
        
        # Process events to calculate share counts
        events = sorted(portfolio[stock], key=lambda x: datetime.strptime(x['event_date'], '%m/%d/%Y %H:%M:%S'))
        
        for date in date_range:
            for event in events:
                event_date = datetime.strptime(event['trade_date'], '%m/%d/%Y')
                if datetime.strptime(date, '%m/%d/%Y') < event_date:
                    stock_shares[stock][date] = current_shares
                elif datetime.strptime(date, '%m/%d/%Y') == event_date:
                    current_shares = event['new_amount']
            stock_shares[stock][date] = current_shares
        
    return stock_shares