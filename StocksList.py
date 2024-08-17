import pandas as pd

# Load the CSV file
file_path = '/Users/sriramsachitchunduri/Desktop/Alpaca-Trading-Bot/Alpaca-Trading-Bot/sp500_companies.csv'
df = pd.read_csv(file_path)

def generatelist(): 
    # Group by 'Sector' and select 4 companies from each sector
    grouped = df.groupby('Sector').apply(lambda x: x.head(4)).reset_index(drop=True)

    # Create a list of all the selected stock symbols
    selected_symbols = grouped['Symbol'].tolist()

    return selected_symbols

# Test the function
print(generatelist())
