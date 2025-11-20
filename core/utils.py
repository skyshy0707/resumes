import datetime
import os

from core.config import Config
from core.schemes.params import Pagination


def now(to_iso=False):
    date = datetime.datetime.now()
    return date.isoformat() if to_iso else date

def is_token_valid(date: str, expires_in: int):
    return date + datetime.timedelta(seconds=expires_in) > now()

def generate_salt():
    return os.urandom(Config.GENERAL_KEY_LENGTH).hex()

def paginate_qs(qs: list, pag_params: Pagination) -> dict:
    limit = pag_params.limit
    offset = pag_params.offset
    items = list(qs)
    return {
        "limit": limit,
        "offset": offset + limit,
        "total": len(items),
        "items": items[offset : limit+offset]
    }
