from sentinelx.database.connection import Base, engine
from sentinelx.database import models, decision_models


def create_tables():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("All SentinelX PostgreSQL tables created successfully.")
