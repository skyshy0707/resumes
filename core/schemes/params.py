from typing import Annotated, Union

from fastapi import Query, Path
from pydantic import Field

from core.schemes.__init__ import BaseModel

class Pagination(BaseModel):
    limit: int = Query(10, gt=0, le=10)
    offset: int = Query(0, ge=0)


class SearchResume(Pagination):


    content: str = Query('')
    title: str = Query('')
