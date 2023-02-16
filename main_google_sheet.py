from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import get_plc_siemens as getPLC

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
# SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_SPREADSHEET_ID = 'put_your_google_sheet_id_here'
# SAMPLE_RANGE_NAME = 'Class Data!A2:E'
SAMPLE_RANGE_NAME = 'put_your_sheet_name_here!A:J'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found on sheet.')
        else:
            print("Show existed data from sheet *** ")
            for row in values:
                print(row)

        # write data
        payload = getPLC.get_plc_db()
        if payload:
            result = getPLC.make_data_for_sheet(payload=payload)
            # Convert False from Python to FALSE (as string) before sending to google sheet
            result[1] = list(map(lambda x: x.replace('False', 'FALSE'), result[1]))

            # Convert True from Python to TRUE (as string) before sending to google sheet
            result[1] = list(map(lambda x: x.replace('True', 'TRUE'), result[1]))
            
            # values = [
            #   ['1', '2'],
            #   ['3', '4']
            # ]

            if values:
                values.append(result[1])
                body = {
                    'values': values
                }
            else:
                body = {
                    'values': result
                }
            res=sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,  
                                        valueInputOption='USER_ENTERED', 
                                        body=body, 
                                        range=SAMPLE_RANGE_NAME).execute()
    except HttpError as err:
        print(f"Error occurred: {err}")


if __name__ == '__main__':
    main()