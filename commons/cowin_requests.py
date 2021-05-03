import requests

from datetime import date
from model.resource.available_center import AvailableCenter


raw_current_date = date.today()
current_date = raw_current_date.strftime("%d-%m-%Y")

COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

pincode = 737101

params = {'pincode': pincode, 'date': current_date}

response_raw = requests.get(url=COWIN_URL, params=params)

response = response_raw.json()

print(response)

centers = response['centers']

applicable_age_limit = 45


def construct_and_send_email(available_centers):
    for available_center in available_centers:
        available_center.print_available_center()


available_center_list = []

for center in centers:
    print("Centre Id: " + str(center['center_id']))
    sessions = center['sessions']

    available_dates = []
    for session in sessions:
        min_age_limit = session['min_age_limit']
        available_capacity = session['available_capacity']
        if min_age_limit == applicable_age_limit and available_capacity > 0:
            available_dates.append(session['date'])

    if len(available_dates) > 0:
        available_center_list.append(AvailableCenter(center['center_id'], center['name'], center['district_name'],
                                                     center['block_name'], center['pincode'], available_dates))


if len(available_center_list) > 0:
    construct_and_send_email(available_center_list)
