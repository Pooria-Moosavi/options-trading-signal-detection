# options-trading-signal-detection

Note: This code is a work in progress and might not run correctly.

Overview
This Python script is designed to analyze stock market data from the Tehran Stock Exchange (TSE) and generate trading signals for stock options. The primary focus is on detecting potential trading opportunities based on the relationship between option prices and underlying stock prices.

Dependencies
pandas
requests
datetime
persiantools.jdatetime
numpy (not imported explicitly in the code, but used internally)
Usage
Clone the repository:


```
git clone https://github.com/Pooria-Moosavi/options-trading-signal-detection.git
```

Install the required dependencies:

```
pip install pandas requests persiantools.jdatetime numpy
```
Run the script:


```
python stock_options_trading.py
```
Review the generated Excel file (market_watch.xlsx) containing stock market data and the trading signals.

Functionality
Data Retrieval:

The script fetches stock market data from the TSE using the URL 'https://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx'.
Data Processing:

The script processes the raw data to extract relevant information and organizes it into a Pandas DataFrame.
Option and Stock Filtering:

The script filters the DataFrame to separate options from stocks based on certain criteria.
Options are further categorized into two types: 'اختيارخ' and 'اختيارف'.
Date Conversion:

Persian dates in the 'Strike Date' column are converted to Gregorian dates using the 'persiantools.jdatetime' library.
Time Difference Calculation:

The time difference between the current date and the strike date is calculated for each option.
Identifier Generation:

Identifiers are created for options and stocks to facilitate matching.
Signal Detection:

Trading signals are generated for 'اختيارخ' options based on a simple comparison of the total option value (premium + strike price) with the stock price.
Important Note
This code is a work in progress and may not function correctly. It is intended for educational purposes and should be used with caution in a real-world trading environment. The trading strategy and signal generation logic need further refinement and validation.

Disclaimer: This code does not constitute financial advice, and the author is not responsible for any financial losses incurred. Use at your own risk.
