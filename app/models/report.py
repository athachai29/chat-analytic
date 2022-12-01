from pydantic import BaseModel


class ReportBase(BaseModel):
    reportCode: str
    filename: str
