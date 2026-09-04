from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
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

from ai_service import (
    build_ai_evaluation_payload,
    evaluate_project_with_ai,
)

from import_service import parse_csv


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


@app.post("/import/csv")
def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="CSV file is required.",
        )

    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        content = file.file.read()
        imported_tasks = parse_csv(content)

        if not imported_tasks:
            raise HTTPException(
                status_code=400,
                detail="CSV file contains no data rows.",
            )

        projects_created = 0
        tasks_created = 0

        project_cache = {}

        for imported_task in imported_tasks:
            project_name = imported_task.project_name

            if project_name not in project_cache:
                project = (
                    db.query(Project)
                    .filter(Project.name == project_name)
                    .first()
                )

                if not project:
                    project = Project(
                        name=project_name,
                        description=(
                            imported_task.project_description
                        ),
                        status=imported_task.project_status,
                    )

                    db.add(project)
                    db.flush()

                    projects_created += 1

                project_cache[project_name] = project

            project = project_cache[project_name]

            task = Task(
                project_id=project.id,
                name=imported_task.task_name,
                description=imported_task.task_description,
                status=imported_task.task_status,
                priority=imported_task.task_priority,
                due_date=imported_task.due_date,
                estimated_hours=imported_task.estimated_hours,
                actual_hours=imported_task.actual_hours,
            )

            db.add(task)
            tasks_created += 1

        db.commit()

        return {
            "projects_created": projects_created,
            "tasks_created": tasks_created,
            "rows_processed": len(imported_tasks),
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as exc:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=f"CSV import failed: {exc}",
        ) from exc

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


@app.get("/projects/{project_id}/ai-payload")
def get_ai_evaluation_payload(
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

    return build_ai_evaluation_payload(
        project=project,
        tasks=tasks,
        delivery_metrics=delivery_metrics,
        overdue_tasks=overdue_tasks,
        effort_metrics=effort_metrics,
        schedule_risk=schedule_risk,
        effort_risk=effort_risk,
        project_health=project_health,
    )