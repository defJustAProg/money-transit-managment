from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a superuser with specified username and password'

    def add_arguments(self, parser):
        parser.add_argument('u', type=str, help='Username for the superuser')
        parser.add_argument('e', type=str, help='Email for the superuser')
        parser.add_argument('p', type=str, help='Password for the superuser')

    def handle(self, *args, **kwargs):
        username = kwargs['username']
        email = kwargs['email']
        password = kwargs['password']

        User = get_user_model()
        User.objects.create_superuser(username=username, email=email, password=password)
