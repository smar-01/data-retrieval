from datetime import datetime

def get_today():

    now = datetime.now()

    # Format the date as "YYYYMMDD"
    formatted_date = now.strftime("%Y%m%d")

    return formatted_date