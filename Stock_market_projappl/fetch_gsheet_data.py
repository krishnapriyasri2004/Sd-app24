import os
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import mysql.connector
from datetime import datetime

# Paths to the credentials and verify their existence
file_path = r'C:\Users\SuryaKrishna\Downloads\stock-data-project-435510-484cf85831bc.json'
directory_path = os.path.dirname(file_path)

if not os.path.isdir(directory_path):
    print("Directory does not exist:", directory_path)
else:
    print("Directory exists.")

if not os.path.isfile(file_path):
    print("File does not exist:", file_path)
else:
    print("File exists.")

# Fetch data from Google Sheets
if os.path.isfile(file_path):
    try:
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly',
                  'https://www.googleapis.com/auth/drive.readonly']

        creds = Credentials.from_service_account_file(file_path, scopes=SCOPES)
        client = gspread.authorize(creds)

        sheet_url = 'https://docs.google.com/spreadsheets/d/1GHUTZjrkMFnzzb9arnqOy1Hk6nHfhU4kWazpYSvW8Qg/edit?gid=1903683265'
        sheet = client.open_by_url(sheet_url).sheet1

        all_values = sheet.get_all_values()
        print("Fetched values from Google Sheets:")

        # Process data and ensure it has the correct headers
        expected_headers = ['Symbols', 'Multi Months View', 'Multi Weeks View', 'Weekly View', 'Day View']
        
        # Adjust the number of columns to match expected headers
        data_rows = [row[:len(expected_headers)] for row in all_values if len(row) >= len(expected_headers)]
        
        if len(data_rows) > 0:
            df = pd.DataFrame(data_rows[1:], columns=expected_headers)  # Skip the header row
            print(df.head())

            # Print the date and number of rows fetched
            fetch_date = datetime.now().date()
            num_rows_fetched = len(df)
            print(f"Fetched data for date: {fetch_date}")
            print(f"Number of rows fetched: {num_rows_fetched}")

            # Ensure 'Date' and 'Time' columns
            df['Date'] = fetch_date
            df['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Store full timestamp

            # Database configuration
            config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'rootkp',
                'database': 'stock_data_db'
            }

            conn = mysql.connector.connect(**config)
            cursor = conn.cursor()

            # Create an 'INSERT' query
            insert_query = """
            INSERT INTO stock_data (Symbols, Multi_Months_View, Multi_Weeks_View, Weekly_View, Day_View, Date, Time)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            Multi_Months_View=VALUES(Multi_Months_View),
            Multi_Weeks_View=VALUES(Multi_Weeks_View),
            Weekly_View=VALUES(Weekly_View),
            Day_View=VALUES(Day_View),
            Date=VALUES(Date),
            Time=VALUES(Time)
            """

            # Convert DataFrame rows to tuples
            data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]
            cursor.executemany(insert_query, data_tuples)
            conn.commit()
            print("Data successfully inserted into MySQL")

            cursor.close()
            conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")
