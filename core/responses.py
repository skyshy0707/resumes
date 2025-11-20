from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, RedirectResponse

from core.config import Config

BASE_URL_FRONTEND = Config.BASE_URL_FRONTEND
BASE_URL_API = Config.BASE_URL_API

def raise_(http_exc: HTTPException):
    raise http_exc


UPDATED = lambda content: JSONResponse(
    content=content,
    status_code=status.HTTP_200_OK
)

CREATED = lambda content: JSONResponse(
    content=content,
    status_code=status.HTTP_201_CREATED
)

REDIRECT = lambda url: RedirectResponse(
    url=url,
    status_code=status.HTTP_302_FOUND,
    headers={
        "location": url
    }
)

DATA_ERROR = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=f"Request operation is failed. Detail: {detail}."
    )
)

UNAUTHORIZED = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Fail to authorize. Detail: {detail}."
    )
)

FORBIDDEN = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"Access denied. Detail: {detail}"
    )
)

NOT_FOUND = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Access denied. Detail: {detail}"
    )
)

CONFLICT = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=f"{detail}"
    )
)

GONE = lambda detail: raise_(
    HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=f"{detail}"
    )
)

class redirect_urls:

    site_home = f"{BASE_URL_FRONTEND}/signup"
    refresh_token = f"{BASE_URL_API}/refresh-token"