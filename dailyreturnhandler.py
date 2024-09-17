def load_daily_return_total(daily_value_total):
    """
    Calculates the daily return for each security by comparing its value to the previous day's value.

    Args:
        daily_value_total (dict): A dictionary where keys are security names, 
                                  and values are dictionaries with dates as keys and the daily value as values.

    Returns:
        dict: A dictionary with the same structure as the input, 
              where the values represent the daily return for each security compared to the previous day.
    """

    daily_profit_total = {}

    # Iterate through each equity in the original dictionary
    for equity, daily_values in daily_value_total.items():
        daily_profit_total[equity] = {}  # Initialize the subdictionary for each equity
        
        # Get a list of dates sorted to maintain order
        sorted_dates = sorted(daily_values.keys())
        
        # Iterate through each date
        for i, date in enumerate(sorted_dates):
            if i == 0:
                # No day before, set the difference to 0
                daily_profit_total[equity][date] = 0.0
            else:
                # Calculate the difference with the previous day
                current_value = daily_values[date]
                previous_value = daily_values[sorted_dates[i - 1]]
                daily_profit_total[equity][date] = current_value - previous_value

    return daily_profit_total