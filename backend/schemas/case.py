from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel


class Base(BaseModel):
    pass


class Case(Base):
    case_name: str
    id: int
    short_title: str
    jurisdiction: str
    jurisdiction_id: int
    court: str
    court_id: int
    docket_number: str
    reporter_volume: str
    reporter: str
    reporter_id: int
    first_page: str
    date_decided: date
    citation: str
    case_type: str
    frontend_pdf_url: AnyUrl
    summary: Optional[str] | None = None


class CaseQuery(Base):
    case_name: str
    citation: str
    id: int
