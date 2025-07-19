import os
import django
import io
from django.core.management import call_command

# Set the environment variable so Django knows which settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thebyline.settings")
django.setup()

# Dump data with UTF-8 encoding
with io.open("data.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", format="json", indent=2, stdout=f)
