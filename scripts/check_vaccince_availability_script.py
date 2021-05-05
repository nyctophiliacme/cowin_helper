import csv
import os
import time
from commons.cowin_requests import send_vaccine_availabily_if_applicable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'users.csv')
row_number = 1
with open(file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    print("-----Starting job-----\n")
    for row in csv_reader:
        print("Calculating for user: " + row['Email Address'])
        if row['Age'] == '18 - 44':
            applicable_age_limit = 18
        elif row['Age'] == '45+':
            applicable_age_limit = 45

        raw_pin_codes_list = row['Pin Code(s)'].split(',')
        pin_codes = [int(raw_pin_code) for raw_pin_code in raw_pin_codes_list]

        send_vaccine_availabily_if_applicable(row['Email Address'], row['Name'], pin_codes, applicable_age_limit)
        row_number += 1
        if row_number % 100 == 0:
            print("Calculated for 100 users. Sleeping for a while to throttle requests.")
            time.sleep(600)
