import pandas as pd
from datetime import datetime

def price_storage_contract(injection_dates, withdrawal_dates, 
                           purchase_prices, sale_prices, 
                           injection_rate, withdrawal_rate, 
                           max_storage, storage_cost, 
                           injection_withdrawal_cost, transportation_cost):
    """
    Function to price a natural gas storage contract.

    Args:
        injection_dates (list of str): Dates when the gas is injected (purchase).
        withdrawal_dates (list of str): Dates when the gas is withdrawn (sale).
        purchase_prices (list of float): Prices of gas on the injection dates.
        sale_prices (list of float): Prices of gas on the withdrawal dates.
        injection_rate (float): Rate of gas injection per day (MMBtu/day).
        withdrawal_rate (float): Rate of gas withdrawal per day (MMBtu/day).
        max_storage (float): Maximum storage capacity (MMBtu).
        storage_cost (float): Storage cost per month or per MMBtu.
        injection_withdrawal_cost (float): Cost per injection/withdrawal operation.
        transportation_cost (float): Transportation cost (per injection/withdrawal event).

    Returns:
        float: The value of the storage contract.
    """
    
    # Convert date strings to datetime objects
    injection_dates = pd.to_datetime(injection_dates)
    withdrawal_dates = pd.to_datetime(withdrawal_dates)
    
    # Ensure dates are sorted
    all_dates = sorted(set(injection_dates) | set(withdrawal_dates))
    
    volume = 0
    total_purchase_cost = 0
    total_sales_revenue = 0
    total_storage_cost = 0
    total_injection_withdrawal_cost = 0
    total_transportation_cost = 0
    
    for i in range(len(all_dates)):
        current_date = all_dates[i]
        
        if current_date in injection_dates:
            index = list(injection_dates).index(current_date)
            if volume <= max_storage - injection_rate:
                volume += injection_rate
                total_purchase_cost += injection_rate * purchase_prices[index]
                total_injection_withdrawal_cost += injection_withdrawal_cost
                total_transportation_cost += transportation_cost
            else:
                print(f'Insufficient storage space on {current_date}')
                
        if current_date in withdrawal_dates:
            index = list(withdrawal_dates).index(current_date)
            if volume >= withdrawal_rate:
                volume -= withdrawal_rate
                total_sales_revenue += withdrawal_rate * sale_prices[index]
                total_injection_withdrawal_cost += injection_withdrawal_cost
                total_transportation_cost += transportation_cost
            else:
                print(f'Insufficient gas stored on {current_date}')
    
    # Calculate storage costs
    storage_duration = pd.date_range(start=injection_dates.min(), end=withdrawal_dates.max(), freq='M').size
    total_storage_cost = storage_cost * storage_duration
    
    # Calculate the net contract value
    contract_value = (total_sales_revenue 
                      - total_purchase_cost 
                      - total_storage_cost 
                      - total_injection_withdrawal_cost 
                      - total_transportation_cost)
    
    return contract_value

# Example usage
injection_dates = ['2023-05-01', '2023-05-02', '2023-05-03']
withdrawal_dates = ['2023-11-01', '2023-11-02', '2023-11-03']
purchase_prices = [2.0, 2.1, 2.2]
sale_prices = [3.0, 3.1, 3.2]
injection_rate = 1e6
withdrawal_rate = 1e6
max_storage = 3e6
storage_cost = 100000
injection_withdrawal_cost = 10000
transportation_cost = 50000

contract_value = price_storage_contract(injection_dates, withdrawal_dates, 
                                        purchase_prices, sale_prices, 
                                        injection_rate, withdrawal_rate, 
                                        max_storage, storage_cost, 
                                        injection_withdrawal_cost, transportation_cost)

print(f"The value of the contract is: ${contract_value:,.2f}")
