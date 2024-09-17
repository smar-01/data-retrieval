from datetime import datetime, timedelta
import pandas as pd

def export_dict_to_excel(path,dict):
    """
    Useful for testing dicts to excel.
    """
    all_dates = set()
    for stock_data in dict.values():
        all_dates.update(stock_data.keys())

    all_dates = sorted(all_dates, key=lambda date: datetime.strptime(date, '%m/%d/%Y'))

    df = pd.DataFrame(index=all_dates)

    # Fill the DataFrame with stock data
    for stock, stock_data in dict.items():
        df[stock] = df.index.map(stock_data).fillna(0.0)

    # Export to Excel
    df.to_excel(path, engine='openpyxl')


def parse_date(date_str):
    """
    Try to parse a date string with multiple formats.
    
    Parameters:
        date_str (str): The date string to parse.
    
    Returns:
        datetime: The parsed date.
    
    Raises:
        ValueError: If date_str does not match any known format.
    """
    for fmt in ('%m/%d/%Y', '%Y-%m-%d'):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date string '{date_str}' does not match known formats.")

def export_dict_list_to_excel(path,dict_list):
    """
    Export a list of dictionaries to different sheets in a single Excel file.
    
    Parameters:
    path: path to dump data.
    dict_list (list of dict): List of dictionaries to export.
    """


    with pd.ExcelWriter(path, engine='openpyxl') as writer:
        for i, dict_ in enumerate(dict_list):
            all_dates = set()
            for stock_data in dict_.values():
                all_dates.update(stock_data.keys())

            all_dates = sorted(all_dates, key=parse_date)

            df = pd.DataFrame(index=all_dates)

            # Fill the DataFrame with stock data
            for stock, stock_data in dict_.items():
                df[stock] = df.index.map(stock_data).fillna(0.0)

            # Write DataFrame to a new sheet
            sheet_name = f'Sheet{i+1}'
            df.to_excel(writer, sheet_name=sheet_name)