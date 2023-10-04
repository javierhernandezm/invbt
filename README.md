# ART Investment-Strategy-Backtester:

## Introduction
Welcome to Investment-Strategy-Backtester, a robust open-source library designed to aid in the crafting and evaluation of investment strategies. Built, maintained and used by Alpha Rho Technologies LLC.

## Features
- **Versatility**: Backtest any investment strategy, whether traditional or unconventional.
- **Flexibility**: Test across a range of timeframes, from intraday to multi-year spans.
- **Precision**: Incorporate transaction costs for realistic and accurate simulation results.

## Setup

1. ### **Prerequisites**:

    - Python 3.6 or higher.
    - `requests` module:
    ```bash
    pip install pandas
    pip install datetime
    pip install numpy
    ```

2. ### **Clone the Repository**:

    ```bash
    git clone https://github.com/Alpha-Rho-Technologies/investment_strategy_backtester

3. ### Navigate to the cloned directory:

    ```bash
    cd path_to_directory
    ```

## How to use:

### **Step 1:** Obtain Asset Price Data in CSV Format
- **File Structure:** Ensure your downloaded data is structured in a table with with dates utilized as the index column and respective asset prices presented in subsequent columns.
- **Content:** The table should encapsulate the historical price data for all portfolio assets, facilitating accurate and comprehensive backtesting.

> **Note:** Ensure the data frequency (e.g., daily, monthly) aligns with your backtesting objectives.

### **Step 2:** Create a Weightings CSV
- **File Structure:** Construct a CSV file wherein the first column enumerates the assets and subsequent columns represent rebalance dates.
- **Content:** Populate the table cells with the corresponding asset weight on each rebalance date.
> **Note:** If needed, refer to the sample files located within the repository's `files` folder, for further guidance.

### **Step 3:** Organize Repository Files
- Place the prepared files into the `files` folder within the repository, adhering to the following naming conventions:
  - Portfolio asset data: `apd.csv`
  - Portfolio weightings at rebalance dates: `portfolios.csv`

### **Step 4:** Execute the Backtest Script
- Initiate the backtesting process by running [`example.ipynb`](example.ipynb) using a Jupyter Notebook interface.

> **Note:** Ensure your working directory is set to the repository location to avoid file path issues.

## **Support**
For any queries or issues, please raise an issue in this repository or contact contact@alpharhotech.com.