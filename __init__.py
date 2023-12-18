__copyright__ = "Copyright (C) 2022 Alpha Rho Techologies LLC"
'''
All rights reserved.

TERMS OF USE:
Permission is hereby granted, free of charge, to any person obtaining a copy of this software for personal, non-commercial use. This includes the rights to use, copy, and modify the software for personal purposes.

The above permission does NOT include the rights to use the software, in whole or in part, for any commercial purposes. Commercial use includes, but is not limited to, any revenue-generating activity, whether direct or indirect, related to the software.

RESTRICTIONS:
1. Redistribution in any form is prohibited.
2. Use in commercial or business environments, or any use for commercial benefit, is strictly prohibited.
3. The software may not be included as a part of any product which has a commercial purpose, whether it is sold or given away for free.

NO WARRANTY:
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED.
'''
from invbt.src.utils import *

def bt(portfolios:pd.DataFrame,apd:pd.DataFrame,balance_freq:str,end_date:dt.date,trans_cost:float,starting_balance:float) -> dict:
    """
    Backtest various investment strategies using historical price data to evaluate portfolio performance over time.

    Parameters:
    - portfolios (pd.DataFrame): A DataFrame containing the asset allocations for different portfolios.
            Each column represents a unique portfolio at a point in time and each row is an asset with its weight over time.
    - apd (pd.DataFrame): Asset Price DataFrame containing historical price data for each asset. 
            Each row represents a date and each column represents the price of an asset.
    - balance_freq (str): The frequency at which the backtester should calculate the strategy balance. 
            Examples include: 'B': Business Days
                            'D': daily,
                            'W': weekly,
                            'M': Monthly,
                            'Q': 'quarterly', etc.
    - end_date (dt.date): The final date to which the backtest should be run. This date should match the balance_freq chosen.
    - trans_cost (float): The transaction cost associated with rebalancing the portfolio, represented as a fraction (e.g., 0.01 for 1%).
    - starting_balance (float): The initial amount of money invested in the portfolio.

    Returns:
    - dict: A dictionary containing the backtest results for each portfolio. Each key is a portfolio identifier, and the 
            value is a pandas series with the portfolio performance over that timeframe.
    """
        
    # Set starting balance:
    balance = starting_balance

    # Standarize end_date:
    try:
        end_date = end_date.date()
    except:
        pass

    # Initialize Object to store balance data:
    all_dates_balance = {}

    # Get rebalance dates from portfolios:
    rebalance_dates = portfolios.columns.date
    returns_start_date = rebalance_dates[0]

    # Used to calculate rebalance costs:
    last_weights = pd.Series(0,index=apd.columns)

    try:
      # Asset price data used in simulation: Resampled to fit rebalance dates without missing %
      sim_price_data = apd.resample('D').last().ffill()
    except Exception as e:
        logging.exception(f'Check balance_freq format! | {e}')

    # Calculate Strategy balance:
    n_rebalances = len(rebalance_dates)
    for reb_n in range(0,n_rebalances):

        portfolio_weights = portfolios.iloc[:,reb_n].dropna()

        # Set Date to with next portfolio rebalance
        try:
            if reb_n+1 < n_rebalances:
                next_port = portfolios.iloc[:,reb_n+1]
                date_to = next_port.name.date()
            else:
                # Check End of simulation
                date_to = end_date

                if returns_start_date == date_to:
                    break
        
        except Exception as e:
            logging.exception(f'ERROR setting BT dates | {e}')
        
        # Filter Simulation Price df to match portfolio rebalance range & assets:
        date_filtered_returns = sim_price_data[portfolio_weights.index].loc[returns_start_date : date_to].pct_change(fill_method=None).dropna()
        
        # Calc transaction cost:
        if trans_cost <= 0:
            reb_cost = 0
        else:
            reb_cost = calculate_rebalance_cost(current_portfolio=portfolio_weights,
                                                prev_portfolio=last_weights,
                                                transaction_cost=trans_cost)  

        # Apply Transaction costs:
        net_balance = round(balance * (1-reb_cost),2)

        # Balance period calculation:
        sim = balance_calc(portfolio_weights=portfolio_weights,
                            balance=net_balance,
                            date_filtered_returns=date_filtered_returns)
        
        balance_df = sim['balance_df'].round(2)
        
        last_weights = sim['last_portfolio']

        # Final Balance:
        balance = balance_df.iloc[-1]
        all_dates_balance[reb_n] = balance_df
        
        # Set date & balance for next sim: 
        returns_start_date = date_to
    
    # Create Balance series:
    bt_balance = pd.concat(all_dates_balance.values())

    # Add initial balance to final balance series:
    start_date = pd.to_datetime(rebalance_dates[0])
    bt_balance[start_date] = starting_balance
    
    # Resample to desired balance frequency:
    bt_balance = bt_balance.sort_index().resample(balance_freq).last().ffill()
    
    return bt_balance