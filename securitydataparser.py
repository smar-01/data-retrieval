import blpapi
from blpapi import Session, SessionOptions
from datetime import datetime

def convert_dates_to_yyyymmdd(date): #or date_list
    """
    Convert a datetime object to a string in YYYYMMDD format.
    """
    if isinstance(date, datetime):
        return date.strftime('%Y%m%d')
    elif isinstance(date, str):
        # Check if the string is already in the correct format
        if len(date) == 8 and date.isdigit():
            return date
        else:
            raise ValueError("String must be in 'YYYYMMDD' format")
    else:
        raise TypeError("Input must be a datetime object or a string in 'YYYYMMDD' format")


def load_security_history(session, security, field, startdate, enddate):
    """
    Retrieves historical data for a given security and field over a specified date range.

    Args:
        session (blpapi.Session): The Bloomberg API session to use for the request.
        security (str): The ticker symbol of the security (e.g., 'AAPL US Equity').
        field (str): The field to retrieve (e.g., 'PX_LAST').
        startdate (str or datetime): The start date of the data request in 'YYYYMMDD' format or as a datetime object.
        enddate (str or datetime): The end date of the data request in 'YYYYMMDD' format or as a datetime object.

    Returns:
        list: A list of lists, where each sublist contains a date (str) and the field value (float).

    Example return:
    [
        ['20240101', 150.50],
        ['20240102', 152.30],
        ...
    ]
    """

    ticker = security
    #assert frequency in ['DAILY', 'WEEKLY', 'MONTHLY', 'QUARTERLY', 'SEMI_ANNUALLY', 'YEARLY']
    fieldname=field # Field variable will be transformed in loop
    frequency = "DAILY"

    session.openService('//blp/refdata')
    refDataService = session.getService('//blp/refdata')
    request = refDataService.createRequest('HistoricalDataRequest')

    if type(ticker) == str:
        tickers = [ticker]
    for ticker in tickers:
        request.getElement('securities').appendValue(ticker)
    if type(field) == str:
        fields = [field]
    for field in fields:
        request.getElement('fields').appendValue(field)
    request.set('periodicitySelection', frequency)

    startdate = convert_dates_to_yyyymmdd(startdate)
    enddate = convert_dates_to_yyyymmdd(enddate)
    request.set('startDate', startdate)
    request.set('endDate', enddate)

    session.sendRequest(request)
    data = []
    while True:
        event = session.nextEvent()
        for msg in event:
            if msg.messageType() == 'HistoricalDataResponse':
                securityData = msg.getElement('securityData')
                fieldData = securityData.getElement('fieldData')
                for element in fieldData:
                    date = (element.getElementAsString('date'))
                    px = (element.getElementAsFloat(fieldname))

                    data.append([date,px])
        if event.eventType() == blpapi.Event.RESPONSE:
            break
        
    return data


