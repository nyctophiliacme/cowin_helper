import requests

from datetime import datetime
from pytz import timezone
from model.resource.available_center import AvailableCenter
from commons.custom_email import send_email_helper

COWIN_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"


def send_vaccine_availabily_if_applicable(user_email_address, user_name, pin_codes, applicable_age_limit):
    available_centers = []
    for pin_code in pin_codes:
        centers = make_cowin_api_request(pin_code)
        if len(check_vaccine_availability_for_age(centers, applicable_age_limit)) > 0:
            # for temp in check_vaccine_availability_for_age(centers, applicable_age_limit):
            #     print(temp.print_available_center())
            available_centers += check_vaccine_availability_for_age(centers, applicable_age_limit)

    if len(available_centers) > 0:
        construct_and_send_email(available_centers, user_email_address, user_name)


def make_cowin_api_request(pin_code):
    require_format = "%d-%m-%Y"
    now_utc = datetime.now(timezone('UTC'))
    now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    current_date = now_asia.strftime(require_format)
    headers_dict = {
        'authority': 'cdn-api.co-vin.in',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'accept': 'application/json, text/plain, */*',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36',
        'origin': 'https://www.cowin.gov.in',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://www.cowin.gov.in/',
        'accept-language': 'en-US,en;q=0.9',
        'if-none-match': 'W/"1ea-+zg9RS/0KwlL1TNVSKyRx9gaUO0"',
    }

    params = {'pincode': pin_code, 'date': current_date}
    response_raw = requests.get(url=COWIN_URL, params=params, headers=headers_dict)
    if response_raw.status_code == 304:
        print('Received 304 response')
        return None
    response = response_raw.json()
    # print(response)
    return response['centers']


def construct_and_send_email(available_centers, receiver_email_address, user_name):
    message_body = construct_email_message(user_name, available_centers)
    print("Sending email to " + receiver_email_address + "\n")
    send_email_helper(receiver_email_address, message_body)


def list_to_string(s):
    # initialize an empty string
    str1 = " "

    # return string
    return (str1.join(s))


def construct_email_message(user_name, available_centers):
    header = 'Hello ' + user_name + ',\nVaccines are available in following centers, dates:\n\n'

    centers_formatted_data = ''
    for available_center in available_centers:
        # available_center.print_available_center()
        centers_formatted_data += 'CenterId: ' + str(available_center.center_id) + '\nCenter Name: ' \
                                + available_center.center_name + '\nAddress: ' + available_center.center_address + \
                                  ', ' + available_center.center_block_name + ', ' + available_center.center_district \
                                  + ', ' + str(available_center.center_pincode) +\
                                '\nDate(s): ' + list_to_string(available_center.available_dates) + '\n\n'

    footer = '''If you find this useful, feel free to share it to your family and friends: https://forms.gle/NHEmAxLzvkX9Cn35A

--------
Developed by Pransh Tiwari

Contact me on:
https://www.linkedin.com/in/pransh-tiwari/
https://github.com/nyctophiliacme
https://www.instagram.com/pransh.tiwari/
--------'''

    return header + centers_formatted_data + footer


def check_vaccine_availability_for_age(centers, applicable_age_limit):
    available_center_list = []
    if centers is None:
        return available_center_list

    for center in centers:
        # print(center['center_id'])
        sessions = center['sessions']

        available_dates = []
        for session in sessions:
            # print(session['date'])
            min_age_limit = session['min_age_limit']
            available_capacity = session['available_capacity']
            if min_age_limit == applicable_age_limit and available_capacity > 0:
                available_dates.append(session['date'])

        if len(available_dates) > 0:
            avaible_center_obj = AvailableCenter(center['center_id'], center['name'], center['district_name'],
                                                 center['block_name'], center['address'], center['pincode'],
                                                 available_dates)
            available_center_list.append(avaible_center_obj)
            # avaible_center_obj.print_available_center()
            # print(available_dates)

    return available_center_list
