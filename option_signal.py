import pandas as pd
import requests
from datetime import datetime
from persiantools.jdatetime import JaliliDate

req = requests.get(url='https://old.tsetmc.com/tsev2/data/MarketWatchPlus.aspx')
text = req.text
main = text.split('@')
main_csv = main[2]
csv = main_csv.split(';')
rows = [row.split(',') for row in csv]
df = pd.DataFrame(rows)
df.to_excel('market_watch.xlsx')

df1 = df[df[3].str.startswith('اختيارخ')]
df2 = df[df[3].str.startswith('اختيارف')]
stock_df = df[~df[22].isin([208,301,304,306,307,308,311,312,320,321,400,403,404,701,706])]

# Split the 'Column4' into option name, strike price, and strike date
df1[['Option Name', 'Strike Price', 'Strike Date']] = df1[3].str.split('-', expand=True)
df2[['Option Name', 'Strike Price', 'Strike Date']] = df2[3].str.split('-', expand=True)
df1['Strike Date'] = df1['Strike Date'].str.replace('/','')
df2['Strike Date'] = df2['Strike Date'].str.replace('/','')

# Convert Persian date to Gregorian date
def convert_date(persian_date):
    if persian_date is not None:
        length_of_result = len(persian_date)
        if len(persian_date) == 6:
            return JalaliDate(int(persian_date[:2]) + 1400, int(persian_date[2:4]), int(persian_date[4:])).to_gregorian()
        elif len(persian_date) == 8:
            return JalaliDate(int(persian_date[:4]), int(persian_date[4:6]), int(persian_date[6:])).to_gregorian()
        else:
            return None
    else:
        print("Date conversion failed.")
  

# Apply the conversion function to the 'Strike Date' column
df1['Strike Date'] = df1['Strike Date'].apply(convert_date)
df2['Strike Date'] = df2['Strike Date'].apply(convert_date)

# Calculate the time distance between now and strike date
df1['Time Differnce'] = (datetime.now() - pd.to_datetime(df1['Strike Date'])) * -1
df2['Time Differnce'] = (datetime.now() - pd.to_datetime(df2['Strike Date'])) * -1

df1['identifier'] = [i[4:8] for i in df1[1]]
df2['identifier'] = [i[4:8] for i in df2[1]]
stock_df['identifier'] = [i[4:8] for i in stock_df[1]]

# Add 'signal' column to df1
df1['signal'] = 0  # Initialize the 'signal' column
df2['signal'] = 0  # Initialize the 'signal' column

for index, option_row in df1.iterrows():
    # Find the corresponding stock based on the identifier
    matching_stock = stock_df[stock_df['identifier'].str.startswith(option_row['identifier'])]

    if not matching_stock.empty:
        stock_row = matching_stock.iloc[0]

        # Calculate total option value (premium + strike price)
        total_option_value = int(option_row[7]) + int(option_row['Strike Price'])

        # Compare total option value with stock price and assign a signal
        df1.at[index, 'signal'] = np.where(total_option_value < int(stock_row[7]), 1, 0)
