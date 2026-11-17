import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect_gspread(json_path: str, spreadsheet_key: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
    gc = gspread.authorize(credentials)
    return gc.open_by_key(spreadsheet_key).sheet1


def main() -> None:
    json_path = os.environ.get("GSPREAD_SERVICE_ACCOUNT_JSON")
    spreadsheet_key = os.environ.get("GOOGLE_SPREADSHEET_KEY")
    if not json_path or not spreadsheet_key:
        raise RuntimeError(
            "Set GSPREAD_SERVICE_ACCOUNT_JSON and GOOGLE_SPREADSHEET_KEY "
            "(see .env.example)."
        )
    ws = connect_gspread(json_path, spreadsheet_key)
    # Example updates — replace with real yield-curve sync logic
    ws.update_cell(1, 1, "test1")


if __name__ == "__main__":
    main()