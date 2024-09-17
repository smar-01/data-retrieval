from datetime import datetime
from typing import Dict

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return as is if the date is already in 'YYYY-MM-DD' format

def load_total_profit_total(
    value_changes_total: Dict[str, Dict[str, float]], 
    daily_return_total: Dict[str, Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    """
    Calculates the total daily profit for each equity by adding the value changes 
    (from buying or selling shares) to the daily returns.

    Args:
        value_changes_total (dict): A dictionary where the keys are stock names, 
                                    and the values are dictionaries with dates and 
                                    the value changes from share transactions.
        daily_return_total (dict): A dictionary where the keys are stock names, 
                                   and the values are dictionaries with dates and 
                                   the daily returns (e.g., from price changes).

    Returns:
        dict: A dictionary where the keys are stock names, and the values are dictionaries 
              with dates as keys and the total profit for each day as values.
    """
    
    total_profit_total = {}

    for equity in value_changes_total:
        total_profit_total[equity] = {}  # Create an empty sub-dictionary for each equity
        
        # Iterate over the dates in value_changes_total for this equity
        for date1, value1 in value_changes_total[equity].items():
            # Format the date from dict1 (value_changes_total) to 'YYYY-MM-DD'
            formatted_date1 = format_date(date1)
            
            # Check if the formatted date exists in daily_return_total with matching format
            if equity in daily_return_total:
                # Format dates in daily_return_total to 'YYYY-MM-DD'
                formatted_daily_returns = {format_date(date): val for date, val in daily_return_total[equity].items()}
                
                # If the date exists in both, add value1 and value2 to calculate total profit
                if formatted_date1 in formatted_daily_returns:
                    value2 = formatted_daily_returns[formatted_date1]
                    # Sum the values from value_changes_total and daily_return_total
                    total_profit_total[equity][formatted_date1] = value1 + value2
    
    return total_profit_total