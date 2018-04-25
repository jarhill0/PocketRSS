from time import mktime

from feedparser import parse

from .util import get_feeds, get_recent_posts, update_recent_posts


def get_new_items(limit=20):
    """Get all new items from feeds on disk."""
    recent_posts = get_recent_posts()
    new_posts = dict()
    feeds = get_feeds()

    num_items = 0

    def finish():
        update_recent_posts(new_posts)

    for feed_url in feeds:
        feed = parse(feed_url)
        feed_title = feed['feed']['title']

        for post in feed['entries']:
            post_time = int(mktime(post['published_parsed']))
            if post_time <= recent_posts.get(feed_url, 0):  # it was published at or before the last post
                break

            new_posts[feed_url] = max(new_posts.get(feed_url, 0), post_time)  # remember the most recent post time
            # uses max() because we might encounter 2 new post times in one run

            tags = [feed_title] + parse_tags(post.get('tags', []))
            yield {'url': post.link, 'tags': ','.join(tags)}
            num_items += 1

            if num_items >= limit:
                finish()
                return

            if not recent_posts.get(feed_url):  # we don't know this feed
                break  # we added one post. That's enough.

    finish()
    return


def parse_tags(tags):
    """Parse a tags object to return a list, with commas escaped."""
    return [t['term'].replace(',', '\,') for t in tags]
