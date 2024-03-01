import re


def get_integer_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("This value must be an integer. Please try again.")

def get_non_numeric_input(prompt):
    while True:
        value = input(prompt)
        if not value.isnumeric():
            return value
        else:
            print("Value cannot be a number. Please try again.")

def get_valid_date(prompt):
    while True:
        value = input(prompt)
        if re.match(r'^\d{2}/\d{2}/\d{4}$', value):
            return value
        else:
            print("Invalid date format. Please use the format dd/mm/yyyy.")