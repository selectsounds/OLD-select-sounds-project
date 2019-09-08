from colorama import Fore
from docx.opc.exceptions import PackageNotFoundError

from infrastructure.switchlang import switch
import services.data_service as dsvc
import services.web_services as wsvc
import services.label_service as lbsvc


def run():
    print()
    print('***************************** WELCOME ***************************')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('a', add_record)
            s.case('g', generate_labels)
            s.case('l', list_records)
            s.case('f', find_record)
            s.case(['x', 'bye', 'exit', 'exit()'], exit_app)
            s.case('?', show_commands)
            s.case('', lambda: None)
            s.default(unknown_command)

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[A]dd a record')
    print('[G]enerate labels file')
    print('[L]ist existing records')
    print('[F]ind record')
    print('[U]pdate record')
    print('[D]elete record')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_record():
    print(' ****************** ADD RECORD ****************** ')

    record_page_url = input('Enter record page url: ')
    if not record_page_url:
        error_msg('Cancelled')
        return
    if not record_page_url.startswith('https://www.discogs.com/'):
        error_msg('\nInvalid discogs.com address entered')
        return

    record_data = wsvc.extract_record_web_page_data(record_page_url)
    print('Found record:')
    print(f' * name          : {record_data["name"]}\n'
          f' * artist        : {record_data["artist"]}\n'
          f' * label         : {record_data["label"]}\n'
          f' * country       : {record_data["country"]}\n'
          f' * release-date  : {record_data["release-date"]}\n'
          f' * genre         : {record_data["genre"]}\n'
          f' * format        : {record_data["format"]}\n'
          f' * size          : {record_data["size"]}\n'
          f' * speed         : {record_data["speed"]}\n'
          f' * tracklist     : {record_data["tracklist"]}\n'
          f' * lowest-price  : {record_data["lowest-price"]}\n'
          f' * median-price  : {record_data["median-price"]}\n'
          f' * highest-price : {record_data["highest-price"]}\n')
    print()
    add_to_db = input('Add to database (y/n)? ').lower().startswith('y')
    if not add_to_db:
        error_msg('Cancelled')
        return

    record_cost = input('Record cost? (If no value added, default will be £1.00) or press "c" to return to menu): ')
    if record_cost.startswith('c'):
        error_msg('Cancelled')
        return

    if record_cost:
        try:
            record_cost = float(record_cost)
        except ValueError:
            error_msg('Could not convert to price')
            return

    if not record_cost:
        record_cost = None

    existing_records = dsvc.check_existing_records(record_data['name'], record_data['artist'])
    if existing_records:
        print(f'There are {len(existing_records)} records with matching name + artist in database')
        list_existing_records = input('List existing record data (y/n)? ').startswith('y')
        if list_existing_records:
            for idx, r in enumerate(existing_records):
                print(f' Record {idx + 1}:\n'
                      f' * name          : {r.name}\n'
                      f' * artist        : {r.artist}\n'
                      f' * label         : {r.label}\n'
                      f' * country       : {r.country}\n'
                      f' * release-date  : {r.release_date}\n'
                      f' * genre         : {r.genre}\n'
                      f' * format        : {r.format}\n'
                      f' * size          : {r.size}\n'
                      f' * speed         : {r.speed}\n'
                      f' * tracklist     : {r.tracklist}\n'
                      f' * lowest-price  : {r.lowest_price}\n'
                      f' * median-price  : {r.median_price}\n'
                      f' * highest-price : {r.highest_price}\n')

        continue_or_cancel = input('Continue anyway (y/n)? ').startswith('y')
        if not continue_or_cancel:
            error_msg('Cancelled')
            return

    record = dsvc.add_record(record_data, cost=record_cost)

    success_msg(f'Record: "{record.name}" by {record.artist} added to database with id {record.id}')


def generate_labels():
    print(' ****************** GENERATE LABEL FILE ****************** ')

    labels_doc = lbsvc.setup_doc_settings()
    if type(labels_doc) == PackageNotFoundError:
        error_msg("No valid labels template file found. Could not create labels file")
        return

    labels_doc_cells = lbsvc.get_label_cells(labels_doc)

    records = lbsvc.read_records_csv_file()
    formatted_records = lbsvc.format_record_data(records)

    for i in range(len(formatted_records)):
        labels_doc_cells[i].text = formatted_records[i]

    lbsvc.save_labels(labels_doc)

    if lbsvc.check_labels_file_exists():
        success_msg('Label file successfully created at src/data/labels.docx')
        return

    error_msg('Error in creating label file')


def list_records():
    print(' ****************** LIST RECORDS ****************** ')

    # TODO: Take starting & end index for listing
    # TODO: Find all records (sorted by date entered) between start and end index
    # TODO: Display found records
    # TODO: Success message

    print(' ****************** NOT IMPLEMENTED ****************** ')


def find_record(show_header=True):
    if show_header:
        print(' ****************** FIND RECORDS ****************** ')

    # TODO: Take record information (name, artist, (other information?)) to search for record
    # TODO: Display record(s) to user
    # TODO: Success message

    print(' ****************** NOT IMPLEMENTED ****************** ')


def update_record():
    print(' ****************** UPDATE RECORDS ****************** ')

    # TODO: Take record information (name, artist, (other information?)) to search for record
    # TODO: Display record(s) to user
    # TODO: Allow user to select one record to update
    # TODO: (FUTURE) Allow user to update multiple / all found records
    # TODO: Take fields to update from user
    # TODO: Take new data for each given field from user
    # TODO: Update record with new data
    # TODO: Success message

    print(' ****************** NOT IMPLEMENTED ****************** ')


def delete_record():
    print(' ****************** DELETE RECORDS ****************** ')

    # TODO: Take record information (name, artist, (other information?)) to search for record
    # TODO: Display record(s) to user
    # TODO: Success message

    print(' ****************** NOT IMPLEMENTED ****************** ')


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    # if state.active_account:
    #     text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
