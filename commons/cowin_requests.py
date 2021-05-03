import requests

from datetime import date
from model.resource.available_center import AvailableCenter
from commons.custom_email import send_email_helper

COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"


def send_vaccine_availabily_if_applicable(user_email_address, user_name, pin_codes, applicable_age_limit, ):
    available_centers = []
    for pin_code in pin_codes:
        centers = make_cowin_api_request(pin_code)
        available_centers.append(check_vaccine_availability_for_age(centers, applicable_age_limit))

    if len(available_centers) > 0:
        construct_and_send_email(available_centers, user_email_address, user_name)


def make_cowin_api_request(pin_code):
    raw_current_date = date.today()
    current_date = raw_current_date.strftime("%d-%m-%Y")

    params = {'pincode': pin_code, 'date': current_date}
    response_raw = requests.get(url=COWIN_URL, params=params)
    response = response_raw.json()

    return response['centers']


def construct_and_send_email(available_centers, receiver_email_address, user_name):
    message_body = construct_email_message(user_name, available_centers)
    send_email_helper(receiver_email_address, message_body)


def construct_email_message(user_name, available_centers):
    header = 'Hello ' + user_name + ',\nVaccines are available in following centers, dates:\n\n'

    centers_formatted_data = ''
    for available_center in available_centers:
        centers_formatted_data += 'CenterId: ' + available_center.center_id + '\nCenter Name: ' \
                                + available_center.center_name + '\nAddress: ' + available_center.center_block_name + \
                                ', ' + available_center.center_district + ', ' + str(available_center.center_pincode) +\
                                '\nDate(s): ' + str(available_center.available_dates) + '\n'

        available_center.print_available_center()

    footer = '''--------
Developed by Pransh Tiwari
https://www.linkedin.com/in/pransh-tiwari/
https://github.com/nyctophiliacme
https://www.instagram.com/pransh.tiwari/
--------'''

    return header + centers_formatted_data + footer


def check_vaccine_availability_for_age(centers, applicable_age_limit):
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

    return available_center_list
