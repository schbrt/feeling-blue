from sqlmodel import SQLModel, Session, create_engine
from models import Metric


class Connector:
    DB_NAME = "sentimentdb.db"

    def __init__(self) -> None:
        sqlite_url = f"sqlite:///{self.DB_NAME}"
        self.engine = create_engine(sqlite_url, echo=True)

        SQLModel.metadata.create_all(self.engine)
    
    def save_metric(self, metric_name, value) -> None:
        with Session(self.engine) as session:
            session.add(
                Metric(
                    metric_name=metric_name,
                    value=value
                )
            )
            session.commit()