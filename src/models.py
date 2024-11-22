import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Metric(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    metric_name: str = Field(index=True)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(datetime.timezone.utc),
        index=True
    ) 
    value: float