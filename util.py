from datetime import datetime, timedelta, timezone
import time


def convert_time(struct_time: time.struct_time) -> datetime:
    """
    time.struct_timeをdatetime.datetime(JST)に変換する
    feedparserがrss(XML)から返す日付がtime.struct_timeだが、そのままでは使いにくい
    """
    jst_zone = timezone(timedelta(hours=+9), 'Asia/Tokyo')
    converted_time = datetime(*struct_time[:6], tzinfo=timezone.utc).astimezone(jst_zone)
    return converted_time