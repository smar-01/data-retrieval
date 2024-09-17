import os
import sessionhandler
import securitydataparser
import portfolioticketshandler
import portfolioshareshandler
import historicalpriceshandler
import visualisationhandler
import securityinfohandler
import sharechangehandler
import valuechangehandler
import dailyvaluehandler
import dailyreturnhandler
import totalprofithandler
import jsonloader
import excelexporter

current_dir = os.path.dirname(__file__)
division = 'COMMODITIES'
shared_data_tickets_dir = os.path.join(current_dir, '..', 'shared-data', 'tickets', division)
shared_data_deposit_dir = os.path.join(current_dir, '..', 'shared-data', 'raw', division)

def start_session():
    session = sessionhandler.start_session()

    if not session:
        print("Failed to start session")
        return False
    
    return session

def build_portfolio(session):
    """
    Generates portfolio
    """

    ticket_file     = 'DALIS COMMODITIES PTD.csv'
    ticket_dir      = os.path.join(shared_data_tickets_dir, ticket_file)
    ticket_limit    = None
    

    # Choose to read data from saved.
    portfolio_tickets_total     = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "portfolio_tickets_total.json"))    
    portfolio_shares_total      = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "portfolio_shares_total.json"))    
    historical_prices_total     = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "historical_prices_total.json"))    
    daily_value_total           = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "daily_value_total.json"))
    share_changes_total         = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "share_changes_total.json"))
    value_changes_total         = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "value_changes_total.json"))
    daily_return_total          = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "daily_return_total.json"))
    total_profit_total          = jsonloader.read_from_file(os.path.join(shared_data_deposit_dir, "total_profit_total.json"))

    
    # Gather and calculate data.
    """portfolio_tickets_total     = portfolioticketshandler.load_portfolio_tickets_total(ticket_dir, ticket_limit)
    #security_info_total        = securityinfohandler.load_security_info_total(path) #Will be used in future to further categorize securities.
    portfolio_shares_total      = portfolioshareshandler.load_portfolio_shares_total(portfolio_tickets_total)
    historical_prices_total     = historicalpriceshandler.load_historical_prices(portfolio_tickets_total,session,"PX_LAST")
    daily_value_total           = dailyvaluehandler.load_daily_value_total(portfolio_shares_total,historical_prices_total)
    share_changes_total         = sharechangehandler.load_share_changes_total(portfolio_shares_total)
    value_changes_total         = valuechangehandler.load_value_changes_total(share_changes_total,historical_prices_total)
    daily_return_total          = dailyreturnhandler.load_daily_return_total(daily_value_total)"""
    #total_profit_total          = totalprofithandler.load_total_profit_total(value_changes_total,daily_return_total)

    # Save data.
    """jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "portfolio_tickets_total.json"), portfolio_tickets_total)    
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "portfolio_shares_total.json"),  portfolio_shares_total)    
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "historical_prices_total.json"), historical_prices_total)    
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "daily_value_total.json"),       daily_value_total)
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "share_changes_total.json"),     share_changes_total)
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "value_changes_total.json"),     value_changes_total)
    jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "daily_return_total.json"),      daily_return_total)"""
    #jsonloader.write_to_file(os.path.join(shared_data_deposit_dir, "total_profit_total.json"),      total_profit_total)


    # Export total portfolio shares and prices to excel. Useful for visualization and testing.
    dict_list = [total_profit_total]
    #dict_list = [portfolio_shares_total,historical_prices_total,daily_value_total,share_changes_total,value_changes_total,daily_return_total]
    excelexporter.export_dict_list_to_excel(os.path.join(shared_data_deposit_dir, "testsheets1.xlsx"),dict_list)


if __name__ == "__main__":
    #session = start_session()
    session = 1

    build_portfolio(session)
