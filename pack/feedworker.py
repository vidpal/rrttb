# -*- coding: utf-8 -*-

import feedparser, sys, re

# return title, url, concat text
def process_feed(feed_url):
    feed = parse_feed(feed_url)
    if feed.status == 301:
        print "Feed " + feed.href  + " changed location. Update location in the configuration file."
    if feed.status == 410:
        print "Feed " + feed.href + " is gone. Remove it from configuration file."
        return None
    if feed.status == 401:
        print "Feed " + feed.href  +  " is password protected. Operation was stopped."
        return None
    if feed.bozo == 1:
        print "Feed " + feed.href + " is not well-formed."
    entries = []
    # try to avoid rubbish marketing posts
    restrict_by_title = re.compile("win|sponsor|sponsored|gift|links|tomorrow|offer|invite|limited|join|us", re.IGNORECASE)
    for entry in feed.entries:
        if "title" in entry and "link" in entry:
            if restrict_by_title.search(entry.title): continue
            new_item = {"title": entry.title.encode('utf-8'), "link":
                    entry.link.encode('utf-8')}
        # feeds may contain post content under different keys  
        if ("content" in entry
                and len(entry.content) > 0 and "value" in entry.content[0]):
            new_item["content"] = entry.content[0].value.encode('utf-8')
        elif "summary" in entry and len(entry.summary) > 0:
            new_item["content"] = entry.summary.encode('utf-8')
        if "content" in new_item: entries.append(new_item)
    return entries
        
def parse_feed(feed_url):
    return feedparser.parse(feed_url)
