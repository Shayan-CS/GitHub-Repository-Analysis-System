import uuid
from sqlalchemy import Column, String, Integer, DateTime, Float, ForeignKey, func, Text, JSON
from app.db.session import Base


def _gen_uuid() -> str:
    return str(uuid.uuid4())


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String(36), primary_key=True, default=_gen_uuid)
    github_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    stars = Column(Integer, nullable=True)
    language = Column(String, nullable=True)
    last_analyzed = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=_gen_uuid)
    repository_id = Column(String(36), ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    summary = Column(Text, nullable=False)
    complexity_score = Column(Float, nullable=False)
    topics = Column(JSON, nullable=True)
    embedding_id = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
