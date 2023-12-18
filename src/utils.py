import logging
import datetime as dt
import pandas as pd
import numpy as np

def balance_calc(portfolio_weights: pd.Series, balance: float, date_filtered_returns: pd.DataFrame) -> dict:
    """
    Simulates a portfolio position balance variation over time.

    Parameters:
    portfolio_weights (pd.Series): The weights of each asset in the portfolio.
    balance (float): The total balance of the portfolio.
    date_filtered_returns (pd.DataFrame): DataFrame of the returns of each asset over time.

    Returns:
    dict: Dictionary containing the balance DataFrame and the last portfolio weights.
    """
    try:
        # If portfolio weights compatible:
        if len(portfolio_weights) != portfolio_weights.isna().sum():
            
            # Calculate the value of each asset in the portfolio
            initial_portfolio = portfolio_weights * balance

            # Calculate cumulative returns over time
            cumulative_log_returns = np.log(1 + date_filtered_returns).cumsum()

            # Calculate the Net Asset Value (NAV) of each asset over time
            position_NAV = (initial_portfolio * np.exp(cumulative_log_returns)).round(2)

            # Calculate the total balance over time
            balance_over_time = position_NAV.sum(axis=1)

            # Calculate the last balance
            final_balance = balance_over_time.iloc[-1]

            # Calculate the weights of the last portfolio
            final_portfolio = position_NAV.iloc[-1] / final_balance
        
        else: # If model weights all nan:

            # Add transaction costs of selling/buying
            dates_index = date_filtered_returns.index
            balance_over_time = pd.Series(balance, index=dates_index)
            final_portfolio = pd.Series(0,index=portfolio_weights.index)

        return {'balance_df': balance_over_time, 'last_portfolio': final_portfolio}
    
    except Exception as e:
        logging.exception(f'ERROR Calculating BT Balance | {e}')

def calculate_rebalance_cost(current_portfolio: pd.Series, prev_portfolio: pd.Series, transaction_cost: float) -> float:
    """
    Calculates the net transaction cost of rebalancing a portfolio.

    Parameters:
    current_portfolio (pd.Series): The weights of each asset in the current portfolio.
    prev_portfolio (pd.Series): The weights of each asset in the last portfolio.
    transaction_cost (float): The transaction cost per unit weight transferred.

    Returns:
    float: The net transaction cost of rebalancing the portfolio.
    """
    try:
        # Calculate the absolute difference in weights between the two portfolios
        weight_difference = abs(current_portfolio - prev_portfolio)

        # Calculate the total transaction cost
        total_cost = (weight_difference * transaction_cost).sum().round(6)

        return total_cost
    
    except Exception as e:
        logging.exception(f'ERROR calculating rebalance costs | {e}')
