
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from agent.config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
SessionLocal = sessionmaker(bind=engine)
