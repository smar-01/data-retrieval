from datetime import datetime


def load_share_changes_total(portfolio_shares_total):
    """
    Calculates the daily changes in shares for each stock in the portfolio.

    Args:
        portfolio_shares_total (dict): A dictionary where the keys are stock names and the values 
                                       are dictionaries with dates as keys and the number of shares held on each day.

    Returns:
        dict: A dictionary where the keys are security names, and the values are dictionaries with dates as keys 
              and the daily change in security as # of securities changed (bought or sole). The first day will 
              always have a value of 0 since there is no previous day to compare to.
    """

    share_changes_total = {}

    # Loop through each equity in the portfolio
    for equity, date_shares in portfolio_shares_total.items():
        changes = {}
        prev_value = None

        # Loop through the dates and shares held on each day
        for date, shares in date_shares.items():
            if prev_value is not None:
                # Calculate the change in shares from the previous day
                changes[date] = shares - prev_value
            else:
                # The first day does not have a previous day to compare to
                changes[date] = 0

            prev_value = shares
        
        # Add the changes dictionary to the result for this equity
        share_changes_total[equity] = changes
    
    return share_changes_total