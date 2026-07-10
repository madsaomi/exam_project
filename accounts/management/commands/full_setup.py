import os, sys
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = "Complete one-command project setup"

    def handle(self, *args, **options):
        self.stdout.write("=" * 50)
        self.stdout.write("  London Project — Full Auto Setup")
        self.stdout.write("=" * 50)

        # 1. Collect static
        self.stdout.write("\n[1/6] Collecting static files...")
        call_command('collectstatic', '--noinput', verbosity=0)
        self.stdout.write("  OK")

        # 2. Migrate
        self.stdout.write("\n[2/6] Running database migrations...")
        call_command('migrate', '--noinput', verbosity=0)
        self.stdout.write("  OK")

        # 3. Load demo data (includes users, categories, dishes, news, about, testimonials, contacts)
        self.stdout.write("\n[3/6] Loading demo data...")
        call_command('load_demo_data')

        # 4. Download images
        self.stdout.write("\n[4/6] Downloading images...")
        call_command('download_images')

        # 5. Check system
        self.stdout.write("\n[5/6] Running system check...")
        call_command('check', verbosity=0)
        self.stdout.write("  No issues found")

        # 6. Summary
        self.stdout.write("\n[6/6] Setup complete!")
        self.stdout.write("=" * 50)
        self.stdout.write("  Admin login:    admin / admin123")
        self.stdout.write("  User login:     user1 / user12345")
        self.stdout.write("  Staff panel:    /staff/")
        self.stdout.write("  API docs:       /api/docs/")
        self.stdout.write("  Site pages:     /pages/")
        self.stdout.write("=" * 50)
