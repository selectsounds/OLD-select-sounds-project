import datetime

from colorama import Fore
from dateutil import parser

from infrastructure.switchlang import switch
import infrastructure.state as state
import services.data_service as svc


def run():
    print(' ****************** Welcome host **************** ')
    print()

    show_commands()

    while True:
        action = get_action()

        with switch(action) as s:
            s.case('c', create_account)
            s.case('a', log_into_account)
            s.case('l', list_cages)
            s.case('r', register_cage)
            s.case('u', update_availability)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')
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
    print('[C]reate an account')
    print('Login to your [a]ccount')
    print('[L]ist your cages')
    print('[R]egister a cage')
    print('[U]pdate cage availability')
    print('[V]iew your bookings')
    print('Change [M]ode (guest or host)')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def create_account():
    print(' ****************** REGISTER **************** ')

    name = input('Name: ')
    email = input('Email: ').strip().lower()

    if svc.find_account_by_email(email):
        error_msg(f"Account with email '{email}' already exists")
        return

    state.active_account = svc.create_account(name, email)
    success_msg(f"Account with id '{state.active_account.id}' registered successfully")


def log_into_account():
    print(' ****************** LOGIN **************** ')

    email = input('Email: ').strip().lower()
    found_account = svc.find_account_by_email(email)

    if not found_account:
        error_msg(f"No account found with email '{email}'")
        return

    state.active_account = found_account
    success_msg(f"Successfully logged into account. Welcome {state.active_account.name}!")


def register_cage():
    print(' ****************** REGISTER CAGE **************** ')

    if not state.active_account:
        error_msg("Must be logged in to register a cage")
        return

    metres = input('How many square metres is the cage? ')
    if not metres:
        error_msg('Cancelled - no input given')
        return

    metres = float(metres)
    carpeted = input('Is it carpeted (y/n)? ').lower().startswith('y')
    has_toys = input('Does it have toys (y/n)? ').lower().startswith('y')
    dangerous_snakes_allowed = input('Dangerous snakes allowed (y/n)? ').lower().startswith('y')
    name = input('Name of cage: ')
    price = float(input('Cage price: '))

    cage = svc.register_cage(
        state.active_account, name, price, metres, carpeted, has_toys, dangerous_snakes_allowed
    )

    state.reload_account()
    success_msg(f"New Cage {name} successfully registered with id '{cage.id}")


def list_cages(suppress_header=False):
    if not suppress_header:
        print(' ******************     Your cages     **************** ')

    if not state.active_account:
        error_msg("Must be logged in to register a cage")
        return

    cages = svc.find_cages_for_user(state.active_account)
    print(f"You have '{len(cages)}' cages")
    for idx, c in enumerate(cages):
        print(f" * {idx + 1}. {c.name} is {c.square_metres}m\N{SUPERSCRIPT TWO}")
        for b in c.bookings:
            print('\t  *  Booking: {}, {} days, booked: {}'.format(
                b.check_in_date, (b.check_out_date - b.check_in_date).days,
                "yes" if b.booked_date else "no"))


def update_availability():
    print(' ****************** Add available date **************** ')

    if not state.active_account:
        error_msg("Must be logged in to update availability")
        return

    list_cages(suppress_header=True)

    cage_number = input("Enter cage number: ")
    if not cage_number:
        error_msg("Cancelled")
        return

    cage_number = int(cage_number)
    cages = svc.find_cages_for_user(state.active_account)
    selected_cage = cages[cage_number - 1]

    success_msg(f"Selected cage {selected_cage.name}")

    start_date = parser.parse(
        input("Enter date cage will be available from [yyyy-mm-dd]: ")
    )
    days = int(input('How many days will the cage be available for? '))

    svc.add_available_date(
        selected_cage,
        start_date,
        days
    )
    state.reload_account()

    success_msg(f'Date added to cage {selected_cage.name}')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        error_msg("Must be logged in to register a cage")
        return

    cages = svc.find_cages_for_user(state.active_account)

    bookings = [
        (c, b)
        for c in cages
        for b in c.bookings
        if b.booked_date is not None
    ]

    print("You have {} bookings.".format(len(bookings)))
    for c, b in bookings:
        print(' * Cage: {}, booked date: {}, from {} for {} days.'.format(
            c.name,
            datetime.date(b.booked_date.year, b.booked_date.month, b.booked_date.day),
            datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day),
            b.duration_in_days
        ))


def exit_app():
    print()
    print('bye')
    raise KeyboardInterrupt()


def get_action():
    text = '> '
    if state.active_account:
        text = f'{state.active_account.name}> '

    action = input(Fore.BLUE + text + Fore.WHITE)
    return action.strip().lower()


def unknown_command():
    print("Sorry we didn't understand that command.")


def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)
