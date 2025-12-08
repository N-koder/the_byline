import feedparser
from django.utils.text import slugify
from django.utils import timezone
from .models import ExternalFeed, PressRelease
from .utils import map_category_to_byline
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger('rss')


def extract_image(entry):
    summary_html = getattr(entry, "summary", "")

    if not summary_html:
        return None

    soup = BeautifulSoup(summary_html, "html.parser")
    images = soup.find_all("img")

    if not images:
        return None

    try:
        return images[0].get("src")
    except:
        return None


def parse_date(entry):
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            return timezone.make_aware(
                timezone.datetime(*entry.published_parsed[:6])
            )
    except:
        pass

    return timezone.now()


def fetch_press_releases():
    feeds = ExternalFeed.objects.filter(is_active=True)

    if not feeds.exists():
        logger.info("NO FEEDS FOUND — Cron cannot fetch anything.")
        return

    for feed in feeds:
        logger.info(f"Fetching RSS: {feed.url}")

        parsed = feedparser.parse(feed.url)

        if not parsed.entries:
            logger.info(f"No entries found in feed: {feed.url}")
            continue

        new_count = 0

        for entry in parsed.entries:
            link = getattr(entry, "link", None)
            if not link:
                continue

            if PressRelease.objects.filter(link=link).exists():
                continue

            title = getattr(entry, "title", "Untitled")
            slug = slugify(title)[:60]

            PressRelease.objects.create(
                guid=getattr(entry, "guid", link),
                title=title,
                slug=slug,
                summary=getattr(entry, "summary", ""),
                image=extract_image(entry),
                link=link,
                published_at=parse_date(entry),
                category=map_category_to_byline(feed.target_category),
            )

            new_count += 1

        feed.last_fetched = timezone.now()
        feed.save(update_fields=["last_fetched"])

        logger.info(f"Saved {new_count} new articles from: {feed.url}")
