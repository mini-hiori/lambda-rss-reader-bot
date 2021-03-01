from typing import List

def get_target_url() -> List[str]:
    """
    取得対象にするrssのURLを返却する
    """
    url_list = [
        "https://dev.classmethod.jp/feed",
        "https://blog.serverworks.co.jp/feed"
    ]
    return url_list