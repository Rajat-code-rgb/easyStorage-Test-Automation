import csv
from faker import Faker
import os
from dotenv import load_dotenv
from os.path import join , dirname

fake = Faker()
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

'''TEST CASES PATH'''
TEST_CASES_PATH = os.environ.get('TEST_CASES_PATH')
CREDIT_CARD_FILE_NAME = os.environ.get('CREDIT_CARD_FILENAME')
CREDIT_CARD_FILE_PATH = join(TEST_CASES_PATH, CREDIT_CARD_FILE_NAME)

'''NECESSARY SETTINGS'''
NUMBER_OF_CREDIT_CARD = 1000

# Function to generate dummy credit card data
def generate_credit_card_data(num_cards):
    credit_cards = []
    for _ in range(num_cards):
        credit_cards.append({
            'Card Number': fake.credit_card_number(card_type=None),
            'Card Type': fake.credit_card_provider(),
            'Expiration Date': fake.credit_card_expire(),
            'CVV': fake.credit_card_security_code(),
            'Status': 1
        })
    return credit_cards

# Function to write data to a CSV file
def write_to_csv(filename, data):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Card Number', 'Card Type', 'Expiration Date', 'CVV' , 'Status'])
        writer.writeheader()
        writer.writerows(data)

def main():

    # Generate dummy credit card data
    data = generate_credit_card_data(NUMBER_OF_CREDIT_CARD)
    
    # Write data to CSV
    write_to_csv(CREDIT_CARD_FILE_PATH, data)


if __name__ == '__main__':
    main()
