import feedparser
from django.utils.text import slugify
from django.utils import timezone
from .models import ExternalFeed, PressRelease
from .utils import map_category_to_byline
from bs4 import BeautifulSoup
import json

def extract_image(entry):
    # if "media_content" in entry:
    #     try:
    #         return entry.media_content[0]["url"]
    #     except:
    #         pass

    # if "image" in entry.summary:
    #     return entry.summary["image"]

    # return None

    summary_html = entry.summary
    
    # Parse the HTML
    soup = BeautifulSoup(summary_html, "html.parser")

    # Find all images
    images = soup.find_all("img")

    # Extract the 'src' attribute
    img_urls = [img['src'] for img in images]

    # print(img_urls)
    return img_urls[0]


def parse_date(entry):
    try:
        return timezone.make_aware(
            timezone.datetime(*entry.published_parsed[:6])
        )
    except:
        return timezone.now()


def fetch_press_releases():
    feeds = ExternalFeed.objects.filter(is_active=True)

    for feed in feeds:
        parsed = feedparser.parse(feed.url)

        for entry in parsed.entries:
            # print(json.dumps(entry, indent=4, default=str)) 
            if PressRelease.objects.filter(link=entry.link).exists():
                continue  # avoid duplicates
            
            guid = entry.get("guid", entry.get("link"))
            title = entry.title
            slug = slugify(title)[:60]

            PressRelease.objects.create(
                guid=guid,
                title=title,
                slug=slug,
                summary=getattr(entry, "summary", ""),
                # content=getattr(entry, "content", [{"value": ""}])[0]["value"],
                image=extract_image(entry),
                link=entry.link,
                published_at=parse_date(entry),
                category=map_category_to_byline(feed.target_category),
            )

        feed.last_fetched = timezone.now()
        feed.save(update_fields=["last_fetched"])
