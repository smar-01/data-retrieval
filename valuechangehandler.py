from datetime import datetime
from typing import Dict

def format_date(date_str):
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%Y-%m-%d")
    except ValueError:
        return date_str  # Return as is if the date is already in 'YYYY-MM-DD' format

def load_value_changes_total(
    share_changes_total: Dict[str, Dict[str, int]], 
    historical_prices_total: Dict[str, Dict[str, float]]
) -> Dict[str, Dict[str, float]]:
    """
    Calculates the daily value changes based on share changes and the corresponding security prices.
    
    For example, if 30 shares were sold at a price of 10, the value change is -300, which is recorded as +300 
    since cash is gained. This helps balance out daily profit changes when calculating total profit.

    Args:
        share_changes_total (dict): A dictionary with stock names as keys and dictionaries of daily share changes as values.
        historical_prices_total (dict): A dictionary with stock names as keys and dictionaries of daily prices as values.

    Returns:
        dict: A dictionary where the keys are stock names, and the values are dictionaries with dates as keys
              and the value changes as values. The value is negative if shares were bought and positive if sold.
    """

    value_changes_total = {}

    for equity in share_changes_total:
        value_changes_total[equity] = {}  # Create an empty sub-dictionary for each equity
        
        # Iterate over the dates in dict1 for this equity
        for date1, value1 in share_changes_total[equity].items():
            # Format date from dict2 to match dict1
            formatted_date2 = format_date(date1)
            
            # Check if the formatted date exists in both dict1 and dict2
            if formatted_date2 in historical_prices_total.get(equity, {}):
                value2 = historical_prices_total[equity][formatted_date2]
                # Multiply the values from dict1 and dict2 and store in dict3
                value_changes_total[equity][date1] = -(value1 * value2) #negative flip is necessary
    
    return value_changes_total