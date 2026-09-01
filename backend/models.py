from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(50), nullable=False, default="Not Started")

    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan",
    )


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    status = Column(String(50), nullable=False, default="Not Started")
    priority = Column(String(50), nullable=False, default="Medium")

    due_date = Column(Date, nullable=True)

    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)

    project = relationship(
        "Project",
        back_populates="tasks",
    )