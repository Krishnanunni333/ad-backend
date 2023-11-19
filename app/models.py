from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    Id: int
    Sector: str

class UrlCreate(BaseModel):
    Id: int
    Url: str

class UrlStore(UrlCreate):
    Url: str
    Keywords: list[str]