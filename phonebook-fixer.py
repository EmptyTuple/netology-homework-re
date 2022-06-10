import re
import csv
import itertools
from operator import itemgetter

PHONE_BOOK = "phonebook_raw.csv"

def phonebook_to_list(filename: str) -> list:
    """The function reads csv file and return a list with unstructured lists
       representing persons data.

    Args:
        filename (str): the name of a file to read
    Returns:
        contacts_list (list): list consists of row data lists
    """
    with open(filename) as f:
        rows = csv.reader(f, delimiter=",")
        # headers = next(rows)
        raw_contacts_list = list(rows)
    return raw_contacts_list

def recast_phone_number(phone_number: str) -> str:
    """The function recasts a phone number to the format '+7XXXXXXXXXX доп.XXXX'

    Args:
        phone_number (str): a  raw phone number
    Returns:
        str: the formatted phone number  
    """
    pattern = r'^(?:\+?(?:7|8))[ \-(]*(?P<code>\d{3})[ \-)]*(?P<tel1>\d{3})[ \-]*(?P<tel2>\d{2})[ \-]*(?P<tel3>\d{2})[ (]*(?P<pref>\w{3}\.)* *(?P<ext>\d{4})*\)*$'
    repl = r'+7\g<code>\g<tel1>\g<tel2>\g<tel3> \g<pref>\g<ext>'
    return re.sub(pattern, repl, phone_number).strip()

def recast_contacts(raw_contacts: list)-> list:
    """The function orders all items in contacts

    Args:
        raw_contacts (str): list of raw contatcts

    Returns:
        recasted_contact_list (list): list consists of recasted data lists
    """
    recasted_contact_list = []
    for contact in raw_contacts:
        full_name =[x for x in ' '.join(contact[:3]).split(' ')[:3]]
        recasted_contact = list(itertools.chain(full_name, contact[3:7]))
        recasted_contact[5] = recast_phone_number(contact[5])
        recasted_contact_list.append(recasted_contact)
    return recasted_contact_list

def merge_same_contacts(contacts: list)-> list:
    """The function merges the same contacts

    Args:
        contacts (list): list with ordered contacts lists

    Returns:
        final_list (list): list of uniq contacts lists
    """
    final_dict = {}
    for row in contacts:
        if (row[0], row[1]) not in final_dict.keys():
            final_dict[(row[0], row[1])] = row[2:]
        else:
            final_dict[(row[0], row[1])] = [x if x != '' else y for x, y in zip(final_dict[(row[0], row[1])], row[2:])]
    final_list = []
    for key, value in final_dict.items():
        final_contact = list(key) + (list(value))
        final_list.append(final_contact)
    final_list.sort(key=itemgetter(0, 1))
    return final_list

def write_contacts_csv(final_list: list):
    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(final_list)
       
def main():
    raw_contacts = phonebook_to_list(PHONE_BOOK)
    recasted_contacts = recast_contacts(raw_contacts)
    final_contacts = merge_same_contacts(recasted_contacts)
    write_contacts_csv(final_contacts)
  
if __name__ == '__main__':
    main()
