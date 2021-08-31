from pathlib import Path
import os
import pathlib
from AddressBook import AddressBook

AB = AddressBook()


def add_contact():
    name = input('Enter Name:')
    phone = input('Enter Phone number:')
    if AB.validate_phone(phone):
        AB.add_contact(name, phone)
        return f'Contact {name} with phone number {phone} was created.'
    else:
        return f'Incorrect number. Try in format +380...'


def add_email():
    name = input('Enter Name:')
    email = input('Enter Email:')
    if AB.validate_email(email):
        AB.add_email(name, email)
        return f'{name}`s email {email} has been saved'
    else:
        return f'Incorrect email'


def add_address():
    name = input('Enter Name:')
    address = input('Enter Address:')
    AB.add_address(name, address)
    return f'{name}`s address {address} has been saved'


def add_birthday():
    name = input('Enter Name:')
    birthday = input('Enter Birthday in format 01.01.1990:')
    if AB.validate_birthday(birthday):
        AB.add_birthday(name, birthday)
        return f'{name}`s birthday {birthday} has been saved'
    else:
        return f'Incorrect date'


def change_contact():
    name = input('Enter Name:')
    address = input('Enter address:')
    phone = input('Enter phone:')
    email = input('Enter email:')
    birthday = input('Enter birthday:')
    AB.change_contact(name, address, phone, email, birthday)
    return f'{name}`s :\n Address: {address}, Phone: {phone}, Email: {email}, Birthday: {birthday}'


def find_contact():
    return AB.search(input('Enter search info: '))


def nearby_birthday():
    n_days = input('Enter number of days')
    return AB.nearby_birthday


def delete_contact():
    name = input('Enter Name of the contact: ')
    AB.delete_contact(name)
    return f'Contact {name} was deleted!'


def show_contacts():
    return AB.contacts


OPERATIONS = {
    'add contact': add_contact,
    'add address': add_address,
    'add email': add_email,
    'add birthday': add_birthday,
    'change contact': change_contact,
    'find contact': find_contact,
    'near birthday': nearby_birthday,  # don`t work
    'delete contact': delete_contact,
    'show contacts': show_contacts
}


def get_handler(operator):
    return OPERATIONS[operator]


def main():
    # Start of the cli
    if os.path.exists('data.json'):
        AB.deserialize()
    print('Hello, User!')

    while True:
        command = input('Enter your command: ')
        if command == 'exit':
            AB.serialize()
            break
        handler = get_handler(command)
        answer = handler()
        print(answer)


if __name__ == '__main__':
    main()
