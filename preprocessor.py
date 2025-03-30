import pandas as pd
import re

def preprocess(data):
    # Split the data into lines
    lines = data.split('\n')
    
    # Create a list to hold the processed messages
    messages = []
    
    for line in lines:
        # Regex to match the first format: [DD/MM/YY, HH:MM:SS AM/PM] User: Message
        match1 = re.match(r'\[(\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\s[APMapm]{2})\]\s(.*?):\s(.*)', line)
        
        # Regex to match the second format: DD/MM/YYYY, HH:MM AM/PM - User: Message
        match2 = re.match(r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s(.*?):\s?(.*)', line)
        
        # Regex to match the third format: DD/MM/YYYY, HH:MM AM/PM - User joined...
        match3 = re.match(r'(\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[APMapm]{2})\s-\s([\+0-9\s]+)\s(.*)', line)
        
        if match1:  # First format
            date_time, user, message = match1.groups()
            messages.append([date_time, user.strip(), message.strip()])
        elif match2:  # Second format
            date_time, user, message = match2.groups()
            messages.append([date_time, user.strip(), message.strip()])
        elif match3:  # Third format
            date_time, user, message = match3.groups()
            messages.append([date_time, user.strip(), message.strip()])
        else:
            print(f"No match for line: {line}")  # Debugging line for unmatched lines

    # Create a DataFrame
    df = pd.DataFrame(messages, columns=['date', 'user', 'message'])
    
    # Debugging: Print the number of messages processed
    print(f"Total messages processed: {len(messages)}")
    
    # Convert the 'message' column to string type
    df['message'] = df['message'].astype(str)
    
    # Convert 'date' column to datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %I:%M %p', errors='coerce') \
                  .fillna(pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M:%S %p', errors='coerce'))
    
    # Extract additional features
    df['only_date'] = df['date'].dt.date  # Create 'only_date' column
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    return df
