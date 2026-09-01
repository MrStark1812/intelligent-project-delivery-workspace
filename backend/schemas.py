from datetime import date
from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None
    status: str = "Not Started"


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    status: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    name: str
    description: str | None = None
    status: str = "Not Started"
    priority: str = "Medium"
    due_date: date | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None


class TaskCreate(TaskBase):
    pass


class TaskResponse(TaskBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)