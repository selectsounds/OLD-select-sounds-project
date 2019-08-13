import datetime
from typing import List

import bson

from data.bookings import Booking
from data.cages import Cage
from data.owners import Owner
from data.snakes import Snake


def create_account(name: str, email: str) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email

    owner.save()

    return owner


def find_account_by_email(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner


def register_cage(active_account: Owner, name: str, price: float,
                  metres: float, carpeted: bool, has_toys: bool,
                  dangerous_snakes_allowed: bool) -> Cage:
    cage = Cage()
    cage.name = name
    cage.price = price
    cage.square_metres = metres
    cage.is_carpeted = carpeted
    cage.has_toys = has_toys
    cage.allow_dangerous_snakes = dangerous_snakes_allowed

    cage.save()

    account = find_account_by_email(active_account.email)
    account.cage_ids.append(cage.id)
    account.save()

    return cage


def find_cages_for_user(account: Owner) -> List[Cage]:
    query = Cage.objects(id__in=account.cage_ids)
    cages = list(query)

    return cages


def add_available_date(cage: Cage, start_date: datetime.datetime, days: int):  # -> Cage:
    booking = Booking()
    booking.check_in_date = start_date
    booking.check_out_date = start_date + datetime.timedelta(days=days)

    # cage = Cage.objects(id=cage.id.first())
    cage.bookings.append(booking)
    cage.save()

    # return cage


def add_snake(account: Owner, name: str, species: str,
              length: float, venemous: bool) -> Snake:
    snake = Snake()
    snake.name = name
    snake.species = species
    snake.length = length
    snake.is_venomous = venemous
    snake.save()

    owner = find_account_by_email(account.email)
    owner.snake_ids.append(snake.id)
    owner.save()

    return snake


def get_snakes_for_user(user_id: Owner.id) -> List[Snake]:
    owner = Owner.objects(id=user_id).first()
    snakes = Snake.objects(id__in=owner.snake_ids).all()

    return snakes


def get_available_cages(check_in_date: datetime.datetime, checkout_date: datetime.datetime,
                        snake: Snake) -> List[Cage]:
    min_cage_size = snake.length / 4

    query = Cage.objects() \
        .filter(square_metres__gte=min_cage_size) \
        .filter(bookings__check_in_date__lte=check_in_date) \
        .filter(bookings__check_out_date__gte=checkout_date)

    if snake.is_venomous:
        query.filter(allow_dangerous_snakes=True)

    cages: List[Cage] = query.order_by('price', '-square_metres')

    final_cages = []
    for c in cages:
        for b in c.bookings:
            if b.check_in_date <= check_in_date and b.check_out_date >= checkout_date \
                    and not b.booked_date:
                final_cages.append(c)

    return final_cages


def book_cage(account: Owner, snake: Snake, cage: Cage, check_in_date: datetime.datetime,
              checkout_date: datetime.datetime) -> Cage:
    booking: Booking = None

    for b in cage.bookings:
        if b.check_in_date <= check_in_date and b.check_out_date >= checkout_date \
                and not b.booked_date:
            booking = b
            break

    booking.guest_owner_id = account.id
    booking.guest_snake_id = snake.id
    booking.booked_date = datetime.datetime.now()

    cage.save()

    return cage


def get_bookings_for_user(user_id: bson.ObjectId) -> List[Booking]:
    account = Owner.objects(id=user_id).first()
    booked_cages = Cage.objects() \
        .filter(bookings__guest_owner_id=account.id) \
        .only('bookings', 'name')

    def map_cage_to_booking(cage: Cage, booking: Booking) -> Booking:
        booking.cage = cage
        return booking

    bookings = [
        map_cage_to_booking(c, booking)
        for c in booked_cages
        for booking in c.bookings
        if booking.guest_owner_id == account.id
    ]

    return bookings
