import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Ensure identical data generation every time the script runs
np.random.seed(42)

# Set the starting timeline context for a 3-month block
start_date = datetime(2026, 1, 1)
records = []

# Generate exactly 10,000 unique mock customer transaction logs
for i in range(10000):
    date_offset = np.random.randint(0, 90)
    
    # Simulating QSR peak periods (12-2 PM lunch rush, 5-7 PM dinner rush)
    hour = np.random.choice(
        range(6, 24), 
        p=[0.02, 0.03, 0.05, 0.08, 0.12, 0.05, 0.05, 0.05, 0.05, 0.08, 0.15, 0.12, 0.07, 0.04, 0.02, 0.01, 0.01, 0.00]
    )
    minute = np.random.randint(0, 60)
    order_time = start_date + timedelta(days=date_offset, hours=int(hour), minutes=minute)
    
    order_channel = np.random.choice(['Drive-Thru', 'Front Counter', 'Delivery'], p=[0.60, 0.25, 0.15])
    
    # Injecting intentional NULL values for data cleaning practice
    sales_amount = round(np.random.exponential(scale=25) + 5, 2)
    if sales_amount > 150: 
        sales_amount = np.nan 
    
    # Drive-thru logs with intentional database corruption errors (-999)
    service_time = int(np.random.normal(loc=180, scale=45)) if order_channel == 'Drive-Thru' else np.nan
    if service_time and service_time < 30: 
        service_time = -999 
    
    records.append([order_time, order_channel, sales_amount, service_time])

# Convert memory lists into a structured DataFrame object
df = pd.DataFrame(records, columns=['Timestamp', 'Channel', 'Sales_Amount', 'Service_Time_Secs'])

# Export directly to a comma-separated CSV file in your active workspace
df.to_csv('qsr_sales_data.csv', index=False)
print("--- SUCCESS: 'qsr_sales_data.csv' has been generated in your folder! ---")
