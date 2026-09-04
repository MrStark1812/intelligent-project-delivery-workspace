from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from schemas import AIEvaluationResponse


def get_openai_client():
    if not OPENAI_API_KEY:
        raise RuntimeError(
            "OPENAI_API_KEY is not configured."
        )

    return OpenAI(api_key=OPENAI_API_KEY)


def build_ai_evaluation_payload(
    project,
    tasks,
    delivery_metrics,
    overdue_tasks,
    effort_metrics,
    schedule_risk,
    effort_risk,
    project_health,
):
    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status,
        },
        "metrics": {
            **delivery_metrics,
            "overdue_tasks": len(overdue_tasks),
            **effort_metrics,
            "schedule_risk": schedule_risk,
            "effort_risk": effort_risk,
            "project_health": project_health,
        },
        "tasks": [
            {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": (
                    task.due_date.isoformat()
                    if task.due_date
                    else None
                ),
                "estimated_hours": task.estimated_hours,
                "actual_hours": task.actual_hours,
            }
            for task in tasks
        ],
    }


def evaluate_project_with_ai(payload):
    client = get_openai_client()

    response = client.responses.parse(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": (
                    "You are a project delivery analyst. "
                    "Evaluate the project using only the provided "
                    "project metrics and task information. "
                    "Identify meaningful delivery risks, schedule "
                    "concerns, effort concerns, and problem areas. "
                    "Do not invent facts that are not present in "
                    "the project data."
                ),
            },
            {
                "role": "user",
                "content": str(payload),
            },
        ],
        text_format=AIEvaluationResponse,
    )

    return response.output_parsed