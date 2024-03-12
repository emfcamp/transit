from django.core.management.base import BaseCommand
import darwin.tasks


class Command(BaseCommand):
    help = "Downloads the latest timetable and reference files from Darwin"

    def handle(self, *args, **options):
        darwin.tasks.sync_tt_files.delay()
