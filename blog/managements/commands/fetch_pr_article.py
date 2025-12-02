from django.core.management.base import BaseCommand
from blog.rss_service import fetch_press_releases

class Command(BaseCommand):
    help = "Fetch Press Releases from NewsVoir RSS"

    def handle(self, *args, **kwargs):
        fetch_press_releases()
        self.stdout.write(self.style.SUCCESS("Press Releases fetched successfully"))
