from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Order, Ticket, MovieSession
from django.utils.dateparse import parse_datetime

User = get_user_model()


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        if date:
            created_at = parse_datetime(date)
            order = Order.objects.create(user=user, created_at=created_at)
        else:
            order = Order.objects.create(user=user)

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket_data["movie_session"]
            )
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
            )

        return order


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
