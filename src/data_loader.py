"""
Data loader module for fetching financial data from YFinance.
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    """Class to fetch and manage financial data from YFinance."""
    
    def __init__(self, start_date='2015-01-01', end_date='2026-06-30'):
        """
        Initialize DataLoader with date range.
        
        Parameters:
        -----------
        start_date : str, default='2015-01-01'
            Start date for data extraction
        end_date : str, default='2026-06-30'
            End date for data extraction
        """
        self.start_date = start_date
        self.end_date = end_date
        self.assets = {
            'TSLA': 'Tesla Inc.',
            'BND': 'Vanguard Total Bond Market ETF',
            'SPY': 'S&P 500 ETF'
        }
        self.data = {}
    
    def fetch_data(self, tickers=None):
        """
        Fetch historical data for specified tickers.
        
        Parameters:
        -----------
        tickers : list, optional
            List of ticker symbols to fetch. If None, fetches all assets.
        
        Returns:
        --------
        dict : Dictionary with ticker symbols as keys and DataFrames as values
        """
        if tickers is None:
            tickers = list(self.assets.keys())
        
        print(f"Fetching data for {tickers} from {self.start_date} to {self.end_date}...")
        
        for ticker in tickers:
            try:
                print(f"Fetching {ticker} ({self.assets[ticker]})...")
                stock = yf.download(ticker, start=self.start_date, end=self.end_date)
                stock['Ticker'] = ticker
                self.data[ticker] = stock
                print(f"✓ Successfully fetched {len(stock)} records for {ticker}")
            except Exception as e:
                print(f"✗ Error fetching {ticker}: {str(e)}")
        
        return self.data
    
    def get_closing_prices(self):
        """
        Extract closing prices for all assets as a wide DataFrame.
        
        Returns:
        --------
        pd.DataFrame : DataFrame with dates as index and tickers as columns
        """
        closes = {}
        for ticker, df in self.data.items():
            closes[ticker] = df['Close']
        
        return pd.DataFrame(closes)
    
    def get_returns(self):
        """
        Calculate daily returns for all assets.
        
        Returns:
        --------
        pd.DataFrame : Daily returns DataFrame
        """
        closes = self.get_closing_prices()
        returns = closes.pct_change().dropna()
        return returns