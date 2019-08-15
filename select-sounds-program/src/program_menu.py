import datetime

from colorama import Fore

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as dsvc
import services.web_services as wsvc
from services.recordwebpages import RecordInfoPage


def run():
    print()
    print('***************************** WELCOME ***************************')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('a', add_record)
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

    record = dsvc.add_record(record_data, cost=record_cost)

    success_msg(f'Record: "{record.name}" by {record.artist} added to database with id {record.id}')


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


# def log_into_account():
#     print(' ****************** LOGIN **************** ')
#
#     email = input('Email: ').strip().lower()
#     found_account = svc.find_account_by_email(email)
#
#     if not found_account:
#         error_msg(f"No account found with email '{email}'")
#         return
#
#     state.active_account = found_account
#     success_msg(f"Successfully logged into account. Welcome {state.active_account.name}!")
#
#
# def register_cage():
#     print(' ****************** REGISTER CAGE **************** ')
#
#     if not state.active_account:
#         error_msg("Must be logged in to register a cage")
#         return
#
#     metres = input('How many square metres is the cage? ')
#     if not metres:
#         error_msg('Cancelled - no input given')
#         return
#
#     metres = float(metres)
#     carpeted = input('Is it carpeted (y/n)? ').lower().startswith('y')
#     has_toys = input('Does it have toys (y/n)? ').lower().startswith('y')
#     dangerous_snakes_allowed = input('Dangerous snakes allowed (y/n)? ').lower().startswith('y')
#     name = input('Name of cage: ')
#     price = float(input('Cage price: '))
#
#     cage = svc.register_cage(
#         state.active_account, name, price, metres, carpeted, has_toys, dangerous_snakes_allowed
#     )
#
#     state.reload_account()
#     success_msg(f"New Cage {name} successfully registered with id '{cage.id}")
#
#
# def list_cages(suppress_header=False):
#     if not suppress_header:
#         print(' ******************     Your cages     **************** ')
#
#     if not state.active_account:
#         error_msg("Must be logged in to register a cage")
#         return
#
#     cages = svc.find_cages_for_user(state.active_account)
#     print(f"You have '{len(cages)}' cages")
#     for idx, c in enumerate(cages):
#         print(f" * {idx + 1}. {c.name} is {c.square_metres}m\N{SUPERSCRIPT TWO}")
#         for b in c.bookings:
#             print('\t  *  Booking: {}, {} days, booked: {}'.format(
#                 b.check_in_date, (b.check_out_date - b.check_in_date).days,
#                 "yes" if b.booked_date else "no"))
#
#
# def update_availability():
#     print(' ****************** Add available date **************** ')
#
#     if not state.active_account:
#         error_msg("Must be logged in to update availability")
#         return
#
#     list_cages(suppress_header=True)
#
#     cage_number = input("Enter cage number: ")
#     if not cage_number:
#         error_msg("Cancelled")
#         return
#
#     cage_number = int(cage_number)
#     cages = svc.find_cages_for_user(state.active_account)
#     selected_cage = cages[cage_number - 1]
#
#     success_msg(f"Selected cage {selected_cage.name}")
#
#     start_date = parser.parse(
#         input("Enter date cage will be available from [yyyy-mm-dd]: ")
#     )
#     days = int(input('How many days will the cage be available for? '))
#
#     svc.add_available_date(
#         selected_cage,
#         start_date,
#         days
#     )
#     state.reload_account()
#
#     success_msg(f'Date added to cage {selected_cage.name}')
#
#
# def view_bookings():
#     print(' ****************** Your bookings **************** ')
#
#     if not state.active_account:
#         error_msg("Must be logged in to register a cage")
#         return
#
#     cages = svc.find_cages_for_user(state.active_account)
#
#     bookings = [
#         (c, b)
#         for c in cages
#         for b in c.bookings
#         if b.booked_date is not None
#     ]
#
#     print("You have {} bookings.".format(len(bookings)))
#     for c, b in bookings:
#         print(' * Cage: {}, booked date: {}, from {} for {} days.'.format(
#             c.name,
#             datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
#             datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
#             b.duration_in_days
#         ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.YELLOW + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
