import os.path
import csv

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def main():
    """
    Retrieve events from a specific google calendar
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        cal_id = None
        service = build("calendar", "v3", credentials=creds)
        page_token = None
        while True:
            calendar_list = service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list["items"]:
                if calendar_list_entry["summary"] == "Data - Shared":
                    cal_id = calendar_list_entry["id"]
                    print(f"Calendar id found: {cal_id}.")
                    break
            page_token = calendar_list.get("nextPageToken")
            if not page_token:
                break

        if cal_id is not None:
            events_list = []
            try:
                print("Retrieving events.")
                while True:
                    events = (
                        service.events()
                        .list(calendarId=cal_id, pageToken=page_token)
                        .execute()
                    )
                    for event in events["items"]:
                        event_id = event["id"]
                        event_title = event["summary"]
                        events_list.append({
                            "event_id": event_id,
                            "start_date": event["start"]["date"],
                            "end_date": event["end"]["date"],
                            "title": event_title,
                        })
                    page_token = events.get("nextPageToken")
                    if not page_token:
                        break
                ## Save list as csv
                print("Saving events to csv")
                keys = ["event_id", "start_date", "end_date", "title"]
                output_fname = "raw_events.csv"
                with open(output_fname, "w", newline="") as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writeheader()
                    dict_writer.writerows(events_list)
            except HttpError as error:
                print(f"An error occurred: {error}")
        else:
            print("Calendar was not found")

    except HttpError as error:
        print(f"An error occurred: {error}")
        page_token = None


if __name__ == "__main__":
    main()
