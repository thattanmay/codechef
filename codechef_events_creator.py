from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from bs4 import BeautifulSoup

def web_scrapper(url):
    response = requests.get(url)
    data = BeautifulSoup(response.text, 'html.parser')
    return data

url = 'https://www.codechef.com/contests'
data = web_scrapper(url)
contests = data.find_all(class_='dataTable')[1].find('tbody').find_all('tr')
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    contest_info = []

    for contest in contests:
        details = contest.find_all('td')
        code = details[0].get_text()
        name = details[1].get_text()
        new_url = 'https://www.codechef.com/' + code
        start_date = details[2]['data-starttime']
        end_date = details[3]['data-endtime']

        contest_info.append((code, name, new_url, start_date, end_date))  
    
    with open('stack.txt') as file:
        arr = list(file.read().split('\n'))[:-1]
    with open('stack.txt', 'w') as file:
        for i in contest_info:
            file.write(i[0]+'\n')
            if i[0] not in arr:
                print((i[0]))
                code, name, new_url, start_date, end_date = i
                event = {
                    'summary': code,
                    'location': new_url,
                    'description': name,
                    'colorId': '5',
                    'start': {
                        'dateTime': start_date,
                        'timeZone': 'Asia/Calcutta',
                        },
                    'end': {
                        'dateTime': end_date,
                        'timeZone': 'Asia/Calcutta',
                        }
                    }

                event = service.events().insert(calendarId='primary', body=event).execute()

if __name__ == '__main__':
    main()