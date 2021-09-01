from pathlib import Path
import shutil
import os
import time
from collections import Counter
from prettytable import PrettyTable
import sys
from AddressBook import AddressBook

AB = AddressBook()


def wrong(): return 'Wrong command!'


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
    return f'{name}`s address is {address}'


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
    address = input('Enter Address:')
    phone = input('Enter Phone (+380...):')
    email = input('Enter Email:')
    birthday = input('Enter Birthday (xx.xx.xxxx):')
    AB.change_contact(name, address, phone, email, birthday)
    return f'{name}`s :\n Address: {address}, Phone: {phone}, Email: {email}, Birthday: {birthday}'


def find_contact():
    return AB.search(input('Enter search info: '))


def nearby_birthday():
    n_days = input('Enter number of days: ')
    return AB.nearby_birthday(n_days)


def delete_contact():
    name = input('Enter Name of the contact: ')
    AB.delete_contact(name)
    return f'Contact {name} was deleted!'


def show_contacts():
    pretty_contacts = PrettyTable()
    pretty_contacts.field_names = [
        'Name', 'Address', 'Phone', 'Email', 'Birthday']

    for k, v in AB.contacts.items():
        pretty_contacts.add_row(
            [k, v['Address'], v['Phone'], v['Email'], v['Birthday']])
    return pretty_contacts


def create_new_note():
    tags = input('Enter tags for note(less then 5): ')
    note = input('Enter note text: ')
    data = f'{tags}\n\n{note}'
    t = str(time.time()).split('.')[0]
    filename = t+".txt"  # Name would be similar to 1630063227.txt
    try:
        with open(filename, "w") as file:
            file.write(data)
    except IOError:
        print("File not accessible")
    return f'writing to, {filename}'  # Display in console


def delete_note():
    filename = input("Enter FileName: ")
    path = os.getcwd()
    if os.path.isfile(filename):
        os.remove(os.path.join(path, filename))
        return f'{filename} deleted'
    else:
        return 'wrong FileName'


def note_search():
    note = input('note: ')
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    flist = []

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for filename in files:
        try:
            with open(os.path.join(__location__, filename), encoding='utf-8') as currentFile:
                text = currentFile.readlines()
                # Note we're looking for in the second line, lowercase
                if (note.lower() in text[1].lower()):
                    flist.append(filename[:-4])
        except:
            print(f"{filename} contains less than 2 strings or cannot be opened")

    result = Counter(flist)
    if not result:
        return 'No match!'
    else:
        res = 'Matches in Files:\n'
        for key, value in result.items():
            res += f'{value} : {key}\n'
        return res


def note_update():
    # file_to_open = 'data.txt' #filename input.
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, 'r') as file:
            data = file.readlines()

        print('Current note is:')
        print(data[1][:-1])
        note = input("Update a note: ") + '\n'  # note input
        data[-1] = note
        print(f'Note updated to: {note}')

        with open(file_to_open, 'w') as file:
            file.writelines(data)

    except IOError:
        print("File not accessible")


def pretty_commands():
    table = PrettyTable()
    table.title = 'Use these commands bellow or "exit" to stop work'
    table.field_names = ['ADD INFO', 'CHANGE INFO',
                         'Notes&Tags', 'Additionally']

    table.add_rows(
        [
            ['add contact', 'change contact', 'create note', 'near birthday'],
            ['add address', 'find contact', 'change note', 'search notes by tags'],
            ['add email', 'show contacts', 'change tag', 'search notes by text'],
            ['add birthday', 'delete contact', 'delete note', 'sorting files']
        ]
    )
    return table


def Tag_Search_Helper(tag: str, flist: list, filename: str, text: str):
    # Tag we're looking for in the first line, lowercase
    if tag != '%%%%%%%%%%' and (tag.lower() in text[0].lower()):
        flist.append(filename[:-4])
    return flist


def Tag_Search():
    tags = input('Enter six tags: ')
    tags = tags.split(' ')
    __location__ = os.path.realpath(os.path.join(
        os.getcwd(), os.path.dirname(__file__)))
    flist = []

    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for filename in files:
        try:
            with open(os.path.join(__location__, filename), encoding='utf-8') as currentFile:
                text = currentFile.readlines()
                flist = Tag_Search_Helper(tags[0], flist, filename, text)
                flist = Tag_Search_Helper(tags[1], flist, filename, text)
                flist = Tag_Search_Helper(tags[2], flist, filename, text)
                flist = Tag_Search_Helper(tags[3], flist, filename, text)
                flist = Tag_Search_Helper(tags[4], flist, filename, text)
                flist = Tag_Search_Helper(tags[5], flist, filename, text)

        except:
            print(f"{filename} contains less than 2 strings or cannot be opened")

    result = Counter(flist)
    print("Matches in Files:")
    for key, value in result.items():
        print(f'{value} : {key}')


def Tag_update():
    # file_to_open = 'data.txt' #filename input.
    file_to_open = input('Enter FileName: ')
    try:
        with open(file_to_open, 'r') as file:
            data = file.readlines()

        print('Current tags are:')
        print(data[0][:-1])
        tags = input("Write tags: ") + '\n'  # tags input
        data[0] = tags

        with open(file_to_open, 'w') as file:
            file.writelines(data)

    except IOError:
        print("File not accessible")
    return f'Tags updated to: {tags}'


def sorting_files():

    p = input('Enter to the path to the directory: ')

    print(f'Started in {p}')

    images_list = list()
    video_list = list()
    documents_list = list()
    music_list = list()
    archives_list = list()

    suffix_imeges = ".jpeg", ".png", ".jpg"
    suffix_videos = ".avi", ".mp4", ".mov"
    suffix_documents = ".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"
    suffix_music = ".mp3", ".ogg", ".wav", ".amr"
    suffix_archiv = ".zip", ".tar", ".gztar", ".bztar", ".xztar"

    ignor = "archives", "images", "music", "videos", "documents"

    def normalize(p):

        alphabet = {ord('А'): 'A',
                    ord('Б'): 'B',
                    ord('В'): 'V',
                    ord('Г'): 'G',
                    ord('Д'): 'D',
                    ord('Е'): 'E',
                    ord('Ё'): 'Je',
                    ord('Ж'): 'Zh',
                    ord('З'): 'Z',
                    ord('И'): 'I',
                    ord('Й'): 'Y',
                    ord('К'): 'K',
                    ord('Л'): 'L',
                    ord('М'): 'M',
                    ord('Н'): 'N',
                    ord('П'): 'P',
                    ord('Р'): 'R',
                    ord('С'): 'S',
                    ord('Т'): 'T',
                    ord('У'): 'U',
                    ord('Ф'): 'F',
                    ord('Х'): 'Kh',
                    ord('Ц'): 'C',
                    ord('Ч'): 'Ch',
                    ord('Ш'): 'Sh',
                    ord('Щ'): 'Jsh',
                    ord('Ъ'): 'Z',
                    ord('Ы'): 'Ih',
                    ord('Ь'): 'Jh',
                    ord('Э'): 'Eh',
                    ord('Ю'): 'Ju',
                    ord('Я'): 'Ja',
                    ord('а'): 'a',
                    ord('б'): 'b',
                    ord('в'): 'v',
                    ord('г'): 'g',
                    ord('д'): 'd',
                    ord('е'): 'e',
                    ord('ё'): 'je',
                    ord('ж'): 'zh',
                    ord('з'): 'z',
                    ord('и'): 'i',
                    ord('й'): 'y',
                    ord('к'): 'k',
                    ord('л'): 'l',
                    ord('м'): 'm',
                    ord('н'): 'n',
                    ord('п'): 'p',
                    ord('р'): 'r',
                    ord('с'): 's',
                    ord('т'): 't',
                    ord('у'): 'u',
                    ord('ф'): 'f',
                    ord('х'): 'kh',
                    ord('ц'): 'c',
                    ord('ч'): 'ch',
                    ord('ш'): 'sh',
                    ord('щ'): 'jsh',
                    ord('ъ'): 'z',
                    ord('ы'): 'ih',
                    ord('ь'): 'jh',
                    ord('э'): 'eh',
                    ord('ю'): 'ju',
                    ord('я'): 'ja'}

        for root, dirs, files in os.walk(p):
            for dir in dirs:
                d = os.path.join(root, dir)
                if os.path.exists(d):
                    os.rename(d, d.translate(alphabet))
            for file in files:
                y = os.path.join(root, file)
                if os.path.exists(y):
                    os.rename(y, y.translate(alphabet))

    def serch(p):

        for i in os.listdir(p):
            if i not in ignor:
                if os.path.isdir(p + "\\" + i):
                    serch(p + "\\" + i)

        for root, dirs, files in os.walk(p):
            for file in files:
                i = os.path.join(root, file)
                sort_file(i, file)
                unpuck_archives(i, file)

            for folder in dirs:
                f = os.path.join(root, folder)
                remove_folder(f)

    def creat_folder():

        if len(images_list) != 0:
            if not os.path.exists(p + "\\images"):
                os.mkdir(p + "\\images")

        if len(video_list) != 0:
            if not os.path.exists(p + "\\videos"):
                os.mkdir(p + "\\videos")

        if len(documents_list) != 0:
            if not os.path.exists(p + "\\documents"):
                os.mkdir(p + "\\documents")

        if len(music_list) != 0:
            if not os.path.exists(p + "\\music"):
                os.mkdir(p + "\\music")

        if len(archives_list) != 0:
            if not os.path.exists(p + "\\archives"):
                os.mkdir(p + "\\archives")

    def sort_file(i, file):

        if file.endswith(suffix_imeges):
            if file not in images_list:
                images_list.append(file)
            creat_folder()
            if i != p + "\\images" + "\\" + file:
                os.replace(i, p + "\\images" + "\\" + file)

        elif file.endswith(suffix_videos):
            if file not in video_list:
                video_list.append(file)
            creat_folder()
            if i != p + "\\videos" + "\\" + file:
                os.replace(i, p + "\\videos" + "\\" + file)

        elif file.endswith(suffix_documents):
            if file not in documents_list:
                documents_list.append(file)
            creat_folder()
            if i != p + "\\documents" + "\\" + file:
                os.replace(i, p + "\\documents" + "\\" + file)

        elif file.endswith(suffix_music):
            if file not in music_list:
                music_list.append(file)
            creat_folder()
            if i != p + "\\music" + "\\" + file:
                os.replace(i, p + "\\music" + "\\" + file)

    def remove_folder(f):
        if not os.listdir(f):
            os.removedirs(f)

    def unpuck_archives(i, file):

        if file.endswith(suffix_archiv):
            if file not in archives_list:
                archives_list.append(file)
            creat_folder()
            name_folder_archive = file.split(".")
            shutil.unpack_archive(i, p + "\\archives" +
                                  "\\" + name_folder_archive[0])

    normalize(p)
    serch(p)

    return (f"Sorting files by the specified path {p} completed succesfully!")


OPERATIONS = {
    'add contact': add_contact,
    'add address': add_address,
    'add email': add_email,
    'add birthday': add_birthday,
    'change contact': change_contact,
    'find contact': find_contact,
    'near birthday': nearby_birthday,
    'delete contact': delete_contact,
    'show contacts': show_contacts,
    'create note': create_new_note,
    'delete note': delete_note,
    'change note': note_update,
    'change tag': Tag_update,
    'search notes by tags': Tag_Search,
    'search notes by text': note_search,
    'sorting files': sorting_files,
    'help': pretty_commands
}


def get_handler(operator):
    if not OPERATIONS.get(operator):
        return wrong
    return OPERATIONS[operator]


def main():
    # Start of the cli

    if os.path.exists('data.json'):
        AB.deserialize()
    print('Hello, User! Welcome to our CLI-bot')
    print(pretty_commands())

    while True:
        command = input('Enter your command: ')

        if command == '.' or command == 'exit' or command == 'close':
            AB.serialize()
            print('Goodbye!')
            break
        handler = get_handler(command)
        answer = handler()
        print(answer)


if __name__ == '__main__':
    main()
