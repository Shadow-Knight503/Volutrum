# C:\Users\Leroy\PycharmProjects\Volutrum\database.py
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///C:/Users/Leroy/PycharmProjects/Volutrum/volutrum_platform.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Paste your SQLAlchemy database models here exactly as they were
class ProjectModel(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    raw_idea = Column(Text)

class WorkflowStateModel(Base):
    __tablename__ = "workflow_states"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    current_phase = Column(String)
    status = Column(String)

class AgentArtifactModel(Base):
    __tablename__ = "agent_artifacts"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer)
    phase_name = Column(String)
    artifact_content = Column(Text)
    version = Column(Integer, default=1)


class SystemWorkspaceModel(Base):
    """The absolute source of truth for the singular platform workspace."""
    __tablename__ = "workspace"

    id = Column(Integer, primary_key=True, default=1)  # Always Row 1
    raw_idea = Column(Text, nullable=True)
    current_phase = Column(String, default="scoping")  # scoping, hld, lld, completed
    status = Column(String, default="idle")  # idle, running, held_for_review

    # Unified columns to hold the raw output from each agent cleanly in one place
    scoping_artifact = Column(Text, nullable=True)
    hld_artifact = Column(Text, nullable=True)
    lld_artifact = Column(Text, nullable=True)

# Ensure the tables exist
Base.metadata.create_all(bind=engine)
