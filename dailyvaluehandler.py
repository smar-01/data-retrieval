from datetime import datetime

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return as is if the date is already in 'YYYY-MM-DD' format

def load_daily_value_total(portfolio_shares_total,historical_prices_total):
    """
    Calculates the total value held in each security for each day by multiplying daily share counts 
    with corresponding closing prices.

    Args:
        portfolio_shares_total (dict): A dictionary where the keys are security names, 
                                       and the values are dictionaries with dates and the number of shares held.
        historical_prices_total (dict): A dictionary where the keys are security names, 
                                        and the values are dictionaries with dates and the closing prices.

    Returns:
        dict: A dictionary where the keys are security names, and the values are dictionaries
              with dates and the total value held in that security on that day.
    """

    daily_value_total = {}

    for equity in portfolio_shares_total:
        daily_value_total[equity] = {}  # Create an empty sub-dictionary for each equity
        
        # Iterate over the dates in dict1 for this equity
        for date1, value1 in portfolio_shares_total[equity].items():
            # Format date from dict2 to match dict1
            formatted_date2 = format_date(date1)
            
            # Check if the formatted date exists in both dict1 and dict2
            if formatted_date2 in historical_prices_total.get(equity, {}):
                value2 = historical_prices_total[equity][formatted_date2]
                # Multiply the values from dict1 and dict2 and store in dict3
                daily_value_total[equity][date1] = value1 * value2
    
    return daily_value_total