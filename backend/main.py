from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine
from models import Project, Task
from schemas import (
    ProjectCreate,
    ProjectResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

from intelligence import (
    calculate_delivery_metrics,
    calculate_overdue_tasks,
    calculate_effort_metrics,
    calculate_schedule_risk,
    calculate_effort_risk,
    calculate_project_health,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Intelligent Project Delivery Workspace")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "IPDW backend is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    new_project = Project(
        name=project.name,
        description=project.description,
        status=project.status,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@app.post(
    "/projects/{project_id}/tasks",
    response_model=TaskResponse,
)
def create_task(
    project_id: int,
    task: TaskCreate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    new_task = Task(
        project_id=project_id,
        name=task.name,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        estimated_hours=task.estimated_hours,
        actual_hours=task.actual_hours,
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get(
    "/projects/{project_id}/tasks",
    response_model=list[TaskResponse],
)
def get_tasks(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

@app.put(
    "/projects/{project_id}/tasks/{task_id}",
    response_model=TaskResponse,
)
def update_task(
    project_id: int,
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    existing_task = (
        db.query(Task)
        .filter(
            Task.id == task_id,
            Task.project_id == project_id,
        )
        .first()
    )

    if not existing_task:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    update_data = task.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(existing_task, field, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task


@app.get("/projects/{project_id}/intelligence")
def get_project_intelligence(
    project_id: int,
    db: Session = Depends(get_db),
):
    project = (
        db.query(Project)
        .filter(Project.id == project_id)
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    tasks = (
        db.query(Task)
        .filter(Task.project_id == project_id)
        .all()
    )

    delivery_metrics = calculate_delivery_metrics(tasks)

    overdue_tasks = calculate_overdue_tasks(tasks)

    effort_metrics = calculate_effort_metrics(tasks)

    schedule_risk = calculate_schedule_risk(
        delivery_metrics["completion_percentage"],
        len(overdue_tasks),
    )

    effort_risk = calculate_effort_risk(
        effort_metrics["effort_variance_percentage"],
    )

    project_health = calculate_project_health(
        schedule_risk,
        effort_risk,
    )

    return {
        "project_id": project.id,
        "project_name": project.name,
        **delivery_metrics,
        "overdue_tasks": len(overdue_tasks),
        **effort_metrics,
        "schedule_risk": schedule_risk,
        "effort_risk": effort_risk,
        "project_health": project_health,
    }