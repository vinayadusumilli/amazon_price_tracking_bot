import os
import pathlib
import pandas  # pip install pandas
from dotenv import load_dotenv
from google.auth.transport.requests import Request  # pip install google-api-python-client
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow  # pip install google-auth-httplib2 google-auth-oauthlib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = os.environ.get("MY_SPREADSHEET_ID")
CURRENT_PATH = pathlib.Path(__file__).parent.resolve()


class DataManager:
    """
    'DataManager' manages all the file data user requested amazon links and prices
    """

    def __init__(self) -> None:
        """
        reads csv data file using pandas
        """
        credentials = None
        if os.path.exists(f"{CURRENT_PATH}/token.json"):
            credentials = Credentials.from_authorized_user_file(f"{CURRENT_PATH}/token.json", SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'{CURRENT_PATH}/credentials.json', SCOPES)
                credentials = flow.run_local_server(port=0)
            with open(f"{CURRENT_PATH}/token.json", "w") as token:
                token.write(credentials.to_json())
        self.credentials = credentials

    def get_products(self) -> list:
        """
        Takes pandas dataframe data and convert to dictionary
        :return: data dictionary
        """
        try:
            service = build("sheets", "v4", credentials=self.credentials)
            sheets = service.spreadsheets()
            result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range="products").execute()
            values = result.get("values")
            data = pandas.DataFrame(values[1:], columns=values[0]).set_index("Timestamp")
            products_data = data.to_dict(orient="records")
            return products_data
        except HttpError as error:
            print(error)
