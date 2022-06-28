import feedparser
import time
from util import convert_time
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import List


@dataclass
class RssContent():
    title: str
    url: str
    published_date: datetime


def get_rss(endpoint: str, interval: int = 60) -> List[RssContent]:
    """
    rssのxmlを返すendpoint(url)からrss情報を取得し、必要な情報だけ抜き出す
    interval分以内の記事だけを返す。定期実行はinterval分と同じ間隔にすればよい
    intervalを負数にすると全記事返す(デバッグ用)
    """
    nowtime = datetime.now(timezone(timedelta(hours=+9), 'JST'))
    feed = feedparser.parse(endpoint)
    rss_list: List[RssContent] = []
    for entry in feed.entries:
        if not entry.get("link"):
            continue
        if entry.get("published_parsed"):
            published = convert_time(entry.published_parsed)
        else:
            published = convert_time(entry.updated_parsed)
        if (nowtime - published).total_seconds() // 60 <= interval or interval < 0:
            rss_content = RssContent(
                title=entry.title,
                url=entry.link,
                published_date=published
            )
            rss_list.append(rss_content)
    return rss_list
