from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True)

    timestamp = Column(
        DateTime,
        default=datetime.utcnow
    )

    # Agent Location
    location = Column(String)

    # Availability
    status_code = Column(Integer)

    # Performance
    load_time = Column(Float)
    qr_ready_time = Column(Float)

    # Network
    ttfb = Column(Float)
    dns = Column(Float)
    tcp = Column(Float)
    tls = Column(Float)

    # Core Web Vitals
    fcp = Column(Float)
    lcp = Column(Float)
    cls = Column(Float)

    # Page Metrics
    requests = Column(Integer)
    page_size = Column(Float)

    # Screenshot
    screenshot = Column(String)