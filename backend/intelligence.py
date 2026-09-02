from datetime import date


def calculate_completion_percentage(total_tasks, completed_tasks):
    if total_tasks == 0:
        return 0

    return round((completed_tasks / total_tasks) * 100, 2)


def calculate_overdue_tasks(tasks):
    today = date.today()

    return [
        task
        for task in tasks
        if task.due_date
        and task.due_date < today
        and task.status != "Completed"
    ]


def calculate_effort_metrics(tasks):
    estimated_hours = sum(
        task.estimated_hours or 0
        for task in tasks
    )

    actual_hours = sum(
        task.actual_hours or 0
        for task in tasks
    )

    effort_variance = actual_hours - estimated_hours

    if estimated_hours == 0:
        effort_variance_percentage = 0
    else:
        effort_variance_percentage = (
            effort_variance / estimated_hours
        ) * 100

    return {
        "estimated_hours": round(estimated_hours, 2),
        "actual_hours": round(actual_hours, 2),
        "effort_variance": round(effort_variance, 2),
        "effort_variance_percentage": round(
            effort_variance_percentage,
            2,
        ),
    }


def calculate_schedule_risk(
    completion_percentage,
    overdue_count,
):
    if overdue_count > 0 and completion_percentage < 75:
        return "High"

    if overdue_count > 0 or completion_percentage < 50:
        return "Medium"

    return "Low"


def calculate_effort_risk(effort_variance_percentage):
    if effort_variance_percentage > 20:
        return "High"

    if effort_variance_percentage > 10:
        return "Medium"

    return "Low"


def calculate_project_health(
    schedule_risk,
    effort_risk,
):
    if (
        schedule_risk == "High"
        or effort_risk == "High"
    ):
        return "At Risk"

    if (
        schedule_risk == "Medium"
        or effort_risk == "Medium"
    ):
        return "Needs Attention"

    return "Healthy"


def calculate_delivery_metrics(tasks):
    total_tasks = len(tasks)

    completed_tasks = sum(
        1 for task in tasks
        if task.status == "Completed"
    )

    in_progress_tasks = sum(
        1 for task in tasks
        if task.status == "In Progress"
    )

    not_started_tasks = sum(
        1 for task in tasks
        if task.status == "Not Started"
    )

    completion_percentage = calculate_completion_percentage(
        total_tasks,
        completed_tasks,
    )

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "not_started_tasks": not_started_tasks,
        "completion_percentage": completion_percentage,
    }