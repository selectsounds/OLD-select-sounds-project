from dateutil import parser
import datetime
from data.bookings import Booking
from data.cages import Cage
from infrastructure.switchlang import switch
import program_hosts as hosts
import infrastructure.state as state
from services import data_service as svc


def run():
    print(' ****************** Welcome guest **************** ')
    print()

    show_commands()

    while True:
        action = hosts.get_action()

        with switch(action) as s:
            s.case('c', hosts.create_account)
            s.case('l', hosts.log_into_account)

            s.case('a', add_a_snake)
            s.case('y', view_your_snakes)
            s.case('b', book_a_cage)
            s.case('v', view_bookings)
            s.case('m', lambda: 'change_mode')

            s.case('?', show_commands)
            s.case('', lambda: None)
            s.case(['x', 'bye', 'exit', 'exit()'], hosts.exit_app)

            s.default(hosts.unknown_command)

        state.reload_account()

        if action:
            print()

        if s.result == 'change_mode':
            return


def show_commands():
    print('What action would you like to take:')
    print('[C]reate an account')
    print('[L]ogin to your account')
    print('[B]ook a cage')
    print('[A]dd a snake')
    print('View [y]our snakes')
    print('[V]iew your bookings')
    print('[M]ain menu')
    print('e[X]it app')
    print('[?] Help (this info)')
    print()


def add_a_snake():
    print(' ****************** Add a snake **************** ')

    if not state.active_account:
        hosts.error_msg("Must be logged in to register a cage")
        return

    species = input('Species: ')
    length = float(input('Length (m): '))
    venomous = input('Venomous snake (y/n)? ').startswith('y')

    name = input('Snake name: ')

    snake = svc.add_snake(
        state.active_account,
        name,
        species,
        length,
        venomous
    )

    state.reload_account()
    hosts.success_msg(f'Snake {snake.name} created successfully with id {snake.id}')


def view_your_snakes(show_header=True):
    if show_header:
        print(' ****************** Your snakes **************** ')

    if not state.active_account:
        hosts.error_msg("Must be logged in to register a cage")
        return

    snakes = svc.get_snakes_for_user(state.active_account.id)
    print(f'You have {len(snakes)} snakes')

    for idx, s in enumerate(snakes):
        print(f" {idx + 1}. {s.name} is a {s.species} that is {s.length}m long and is"
              f"{'' if s.is_venomous else ' not'} venomous")

    # for s in snakes:
    #     print(f" * {s.name} "
    #           f"is a {s.species} "
    #           f"that is {s.length}m long and is "
    #           f"{'' if s.is_venomous else 'not '}venomous")


def book_a_cage():
    print(' ****************** Book a cage **************** ')

    if not state.active_account:
        hosts.error_msg("Must be logged in to register a cage")
        return

    snakes = svc.get_snakes_for_user(state.active_account.id)
    if not snakes:
        hosts.error_msg(f'No snakes found for user {state.active_account.name}')
        return

    start_text = input("Check-in date for cage [yyyy-mm-dd]: ")
    if not start_text:
        hosts.error_msg('Cancelled')
        return

    check_in_date = parser.parse(start_text)
    checkout_date = parser.parse(
        input("Checkout date for cage [yyyy-mm-dd]: ")
    )
    if check_in_date >= checkout_date:
        hosts.error_msg('Check in date must be prior to checkout date')
        return

    print('Select snake to book:')
    view_your_snakes(show_header=False)
    snake_number = int(input("Enter snake number: ")) - 1
    snake = snakes[snake_number]

    print('Finding available cages...')
    cages = svc.get_available_cages(check_in_date, checkout_date, snake)

    if not cages:
        hosts.error_msg('No cages available for your date')
        return

    print(f'You have {len(cages)} available cage(s) to book. Please select from the following:')
    for idx, c in enumerate(cages):
        print(f" * {idx + 1}. {c.name}, size: {c.square_metres}m\N{SUPERSCRIPT TWO}, "
              f"carpeted: {'yes' if c.is_carpeted else 'no'}, "
              f"toys: {'yes' if c.has_toys else 'no'}, "
              f"price: {c.price}")

    cage = cages[int(input('Select cage to book: ')) - 1]

    cage = svc.book_cage(
        state.active_account, snake, cage,
        check_in_date, checkout_date
    )

    hosts.success_msg(f'Successfully booked {cage.name} for {snake.name} at £{cage.price}/night')


def view_bookings():
    print(' ****************** Your bookings **************** ')

    if not state.active_account:
        hosts.error_msg("Must be logged in to register a cage")
        return

    snakes = {s.id: s for s in svc.get_snakes_for_user(state.active_account.id)}
    bookings = svc.get_bookings_for_user(state.active_account.id)

    print(f'You have {len(bookings)} booking(s)')
    b: Booking
    for b in bookings:
        hosts.success_msg(f' * Snake: {snakes.get(b.guest_snake_id).name} '
                          f'is booked in cage {b.cage.name} '
                          f'from {datetime.date(b.check_in_date.year, b.check_in_date.month, b.check_in_date.day)} '
                          f'for {(b.check_out_date - b.check_in_date).days} days')
