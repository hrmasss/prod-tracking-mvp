from django.core.management.base import BaseCommand
from seeder.tracker_dev import seed_tracker_data
from seeder.users_dev import seed_users


class Command(BaseCommand):
    help = "Seeds the database with development data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--full",
            action="store_true",
            help="Seed the database with all data (including orders, bundles, etc.)",
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        self.stdout.write("Seeding users...")
        seed_users()
        self.stdout.write(self.style.SUCCESS("Users seeded successfully."))

        self.stdout.write("Seeding tracker data...")
        seed_tracker_data(full=options["full"])
        self.stdout.write(self.style.SUCCESS("Tracker data seeded successfully."))

        self.stdout.write(self.style.SUCCESS("Database seeding complete. 🎉"))
