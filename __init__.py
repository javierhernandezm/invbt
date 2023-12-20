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

def bt(portfolios:pd.DataFrame,apd:pd.DataFrame,balance_freq:str,end_date:dt.date,trans_cost:float,starting_balance:float,annual_kd:float=0) -> dict:
    """
    Backtest long/short investment strategies using historical price data to evaluate portfolio performance over time.

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

    # Get rebalance dates:
    rebalance_dates = portfolios.columns.date

    try:
      # Asset price data used in simulation: Resampled to fit rebalance dates without missing %
      sim_price_data = apd.resample('D').last().ffill()
    except Exception as e:
        logging.exception(f'Check balance_freq format! | {e}')

    # Calculate Strategy balance:
    all_dates_balance = get_balance(starting_balance=starting_balance,portfolios=portfolios,
                                    end_date=end_date,sim_price_data=sim_price_data,
                                    trans_cost=trans_cost,annual_kd=annual_kd,
                                    rebalance_dates=rebalance_dates)
    
    # Create Balance series:
    bt_balance = pd.concat(all_dates_balance.values())

    # Add initial balance to final balance series:
    start_date = pd.to_datetime(rebalance_dates[0])
    bt_balance[start_date] = starting_balance
    
    # Resample to desired balance frequency:
    bt_balance = bt_balance.sort_index().resample(balance_freq).last().ffill()
    
    return bt_balance