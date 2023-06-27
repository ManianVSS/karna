from django.contrib.auth.models import User


def create_super_user():
    try:
        User.objects.get(username='admin')
    except User.DoesNotExist:
        User.objects.create_superuser('admin', 'admin@example.com', 'password')
