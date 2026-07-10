from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates admin user if not exists"

    def handle(self, *args, **options):
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Admin created: admin / admin123'))
        else:
            self.stdout.write('Admin already exists')
