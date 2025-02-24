import pandas as pd

# Read the raw data
raw_df = pd.read_excel('Data w_o analysis.xlsx')

# Convert date columns
raw_df['Purchase_Date'] = pd.to_datetime(raw_df['Date of Purchase'], errors='coerce', unit='ms')
raw_df['Journey_Date'] = pd.to_datetime(raw_df['Date of Journey'], errors='coerce', unit='ms')

# Create Dim_Time
df_time = raw_df[['Purchase_Date', 'Time of Purchase']].copy()
df_time['Date'] = df_time['Purchase_Date'].dt.date
df_time['Day'] = df_time['Purchase_Date'].dt.day
df_time['Month'] = df_time['Purchase_Date'].dt.month
df_time['Year'] = df_time['Purchase_Date'].dt.year
df_time['Time of Day'] = df_time['Time of Purchase']

Dim_Time = df_time.drop_duplicates().reset_index(drop=True)
Dim_Time.insert(0, 'Time ID', range(1, len(Dim_Time) + 1))

# Create Dim_Journey
Dim_Journey = raw_df[['Journey_Date', 'Departure Time', 'Arrival Time', 'Actual Arrival Time', 'Reason for Delay']].copy()
Dim_Journey = Dim_Journey.drop_duplicates().reset_index(drop=True)
Dim_Journey.insert(0, 'Journey ID', range(1, len(Dim_Journey) + 1))

# Create mapping keys
raw_df['time_key'] = raw_df['Purchase_Date'].astype(str) + ' ' + raw_df['Time of Purchase'].astype(str)
raw_df['journey_key'] = (raw_df['Journey_Date'].astype(str) + ' ' + 
                        raw_df['Departure Time'].astype(str) + ' ' + 
                        raw_df['Arrival Time'].astype(str) + ' ' + 
                        raw_df['Actual Arrival Time'].astype(str) + ' ' + 
                        raw_df['Reason for Delay'].astype(str))

Dim_Time['time_key'] = Dim_Time['Purchase_Date'].astype(str) + ' ' + Dim_Time['Time of Day'].astype(str)
Dim_Journey['journey_key'] = (Dim_Journey['Journey_Date'].astype(str) + ' ' + 
                            Dim_Journey['Departure Time'].astype(str) + ' ' + 
                            Dim_Journey['Arrival Time'].astype(str) + ' ' + 
                            Dim_Journey['Actual Arrival Time'].astype(str) + ' ' + 
                            Dim_Journey['Reason for Delay'].astype(str))

# Create mappings
time_mapping = dict(zip(Dim_Time['time_key'], Dim_Time['Time ID']))
journey_mapping = dict(zip(Dim_Journey['journey_key'], Dim_Journey['Journey ID']))

# Create Fact table with proper IDs
Fact_Transactions = raw_df[['Transaction ID', 'Purchase Type', 'Payment Method', 'Railcard', 
                           'Ticket Class', 'Ticket Type', 'Price', 'Journey Status']].copy()

Fact_Transactions['Time ID'] = raw_df['time_key'].map(time_mapping)
Fact_Transactions['Journey ID'] = raw_df['journey_key'].map(journey_mapping)

# Save files
Fact_Transactions.to_csv('Fact_Transactions.csv', index=False)
Dim_Time.to_csv('Dim_Time.csv', index=False)
Dim_Journey.to_csv('Dim_Journey.csv', index=False)

print("Fact Transactions sample (showing Time ID and Journey ID):")
print(Fact_Transactions[['Transaction ID', 'Time ID', 'Journey ID']].head())

print("\
Verifying no null values:")
print("Null Time IDs:", Fact_Transactions['Time ID'].isnull().sum())
print("Null Journey IDs:", Fact_Transactions['Journey ID'].isnull().sum())