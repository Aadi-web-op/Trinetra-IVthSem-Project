"""
Management command to clean up stale AITask records.
Prevents DB bloat from orphaned background tasks.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Removes stale AITask records older than 1 hour to prevent DB bloat'

    def add_arguments(self, parser):
        parser.add_argument(
            '--max-age-minutes',
            type=int,
            default=60,
            help='Delete tasks older than this many minutes (default: 60)'
        )

    def handle(self, *args, **options):
        from officer_portal.models import AITask

        max_age = options['max_age_minutes']
        cutoff = timezone.now() - timedelta(minutes=max_age)

        stale_count = AITask.objects.filter(created_at__lt=cutoff).count()
        if stale_count > 0:
            AITask.objects.filter(created_at__lt=cutoff).delete()
            self.stdout.write(self.style.SUCCESS(
                f'🧹 Cleaned up {stale_count} stale AITask record(s) older than {max_age} minutes.'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('✅ No stale tasks found.'))
