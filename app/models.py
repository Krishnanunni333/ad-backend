from pydantic import BaseModel


class EmployeeCreate(BaseModel):
    Id: int
    Sector: str

class UrlCreate(BaseModel):
    Url: str

class UrlStore(UrlCreate):
    Keywords: list[str]