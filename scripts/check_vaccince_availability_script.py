import csv
import os
from commons.cowin_requests import send_vaccine_availabily_if_applicable

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file_path = os.path.join(BASE_DIR, 'cowin_helper/users.csv')
row_number = 1
with open(file_path) as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    for row in csv_reader:
        question_dict = {
            'question_text': row['question_text'],
            'question_img_url': row['question_img_url'],
        }
        row_number += 1
