import sys
import requests
import traceback
from get_target_url import get_target_url
from get_rss import get_rss
from typing import List
import os
from datetime import datetime, timezone, timedelta
import boto3

ssm = boto3.client('ssm')

def handler(event, context):
    """
    lambda用main関数
    """
    try:
        main()
        return {"result": "OK"}
    except BaseException:
        error_message = traceback.format_exc()
        return {"result": "NG", "error_message": error_message}


def main() -> None:
    """
    handler関数に直接入れてしまうとデバッグ時に使えないのでいったんmainで受ける
    """
    webhook_url = ssm.get_parameter(
        Name='NotifyTrainDelayToSlack-WebhookURL',
        WithDecryption=True
    )
    url_list = get_target_url()
    rss_list: List[RssContent] = []
    for url in url_list:
        rss_list += get_rss(url, interval=60)
    # 得られたrssをサイトの区別なく古い順にソート(とにかく新しい順に投稿)
    rss_list = sorted(rss_list, key=lambda x: x.published_date)
    if len(rss_list) > 0:
        for rss in rss_list:
            content = f"{rss.title}\r{rss.url}\r{rss.published_date}"
            send_webhook(webhook_url, content)
    else:
        message = f"更新なし:{datetime.now(timezone(timedelta(hours=+9), 'JST')).strftime('%Y-%m-%d %H:%M:%S')}"
        send_webhook(webhook_url, message)


def send_webhook(url: str, content: str) -> None:
    """
    指定urlにwebhookを投げて投稿する
    discord想定だが他のサービスでもいける？
    """
    headers = {
        "Content-Type": "application/json"
    }
    content = {
        "content": content
    }
    print(content)
    requests.post(url, headers=headers, json=content, timeout=20)


if __name__ == "__main__":
    main()
