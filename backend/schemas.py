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

class TaskUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: date | None = None
    estimated_hours: float | None = None
    actual_hours: float | None = None


class TaskResponse(TaskBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)


class AIEvaluationResponse(BaseModel):
    health_assessment: str
    risks: list[str]
    schedule_concerns: list[str]
    effort_concerns: list[str]
    problem_areas: list[str]


class ImportTask(BaseModel):
    project_name: str
    project_description: str | None = None
    project_status: str = "Not Started"

    task_name: str
    task_description: str | None = None
    task_status: str = "Not Started"
    task_priority: str = "Medium"

    due_date: date | None = None

    estimated_hours: float | None = None
    actual_hours: float | None = None


class ImportResponse(BaseModel):
    projects_created: int
    tasks_created: int
    rows_processed: int