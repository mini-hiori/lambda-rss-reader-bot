from typing import List
import boto3


def get_target_url() -> List[str]:
    """
    取得対象にするrssのURLを返却する
    """
    # ssmパラメータストアに@区切りでRSS取得対象URLを改行区切りで突っ込んでおく
    url_param: str = ssm.get_parameter(
        Name='RSSURLList'
    )['Parameter']['Value']
    url_param = url_param.replace("\r", "")
    url_list: List[str] = url_param.split("\n")
    return url_list
