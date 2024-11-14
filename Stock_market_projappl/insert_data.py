#insert_data.py
import mysql.connector
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread


credentials_path = 'C:\\Users\\SuryaKrishna\\Desktop\\Stock_market_projapp\\Stock_market_projappl\\stock-data-project-435510-a55d18509619.json'
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1GHUTZjrkMFnzzb9arnqOy1Hk6nHfhU4kWazpYSvW8Qg/edit?gid=1903683265'


SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive.readonly']


creds = Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
client = gspread.authorize(creds)

try:
   
    sheet = client.open_by_url(spreadsheet_url).sheet1
    data = sheet.get_all_values()

    
    header_row_index = 1  
    headers = ['Symbols', 'Multi Months View', 'Multi Weeks View', 'Weekly View', 'Day View']

    
    data_cleaned = [row for row in data if len(row) == len(headers) + 1]  
    df = pd.DataFrame(data_cleaned, columns=headers + ['Extra'])

    
    df = df.drop(columns=['Extra'])
    df.reset_index(drop=True, inplace=True)

    
    df['Date'] = pd.to_datetime('today').date()
    df['Time'] = pd.to_datetime('now').time()

   
    if df.empty:
        print("DataFrame is empty. Check your Google Sheets data.")
        exit()

    
    expected_columns = ['Symbols', 'Multi Months View', 'Multi Weeks View', 'Weekly View', 'Day View', 'Date', 'Time']
    if not all(col in df.columns for col in expected_columns):
        print(f"Missing columns in the DataFrame. Expected columns: {expected_columns}")
        exit()

    data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]

  
    config = {
        'host': 'localhost',
        'user': 'root',         
        'password': 'rootkp',   
        'database': 'stock_data_db'
    }

  
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        print("Database connection successful.")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        exit()

    
    insert_query = """
    INSERT INTO stock_data (Symbols, Multi_Months_View, Multi_Weeks_View, Weekly_View, Day_View, date, time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    try:
        if data_tuples:
            cursor.executemany(insert_query, data_tuples)
            conn.commit()
            print("Data successfully inserted into MySQL")
        else:
            print("No valid data to insert.")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
        conn.close()
        
except Exception as e:
    print(f"Error fetching data: {e}")
