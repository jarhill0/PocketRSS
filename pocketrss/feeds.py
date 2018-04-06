from time import mktime

from feedparser import parse

from .util import get_feeds, get_time, save_time


def get_new_items(limit=20):
    """Get all new items from feeds on disk."""
    last_time = get_time()
    feeds = get_feeds()

    num_items = 0

    def finish():
        save_time()

    for feed_url in feeds:
        feed = parse(feed_url)
        feed_title = feed['feed']['title']

        for post in feed['entries']:
            post_time = mktime(post['published_parsed'])
            if post_time < last_time:
                break
            tags = [feed_title] + parse_tags(post.get('tags', []))
            yield {'url': post.link, 'tags': ','.join(tags)}
            num_items += 1

            if num_items >= limit:
                finish()
                return

    finish()
    return


def parse_tags(tags):
    """Parse a tags object to return a list, with commas escaped."""
    return [t['term'].replace(',', '\,') for t in tags]
