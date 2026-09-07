import csv
import io
from datetime import date, datetime

import pandas as pd

from schemas import ImportTask


REQUIRED_COLUMNS = {
    "project_name",
    "task_name",
}


def normalize_column_name(column: str) -> str:
    return (
        column.strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
    )


def normalize_text(value: str | float | int | None) -> str | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    value = str(value).strip()

    return value if value else None


def normalize_status(value: str | None) -> str:
    value = normalize_text(value)

    if not value:
        return "Not Started"

    status_map = {
        "not started": "Not Started",
        "in progress": "In Progress",
        "completed": "Completed",
        "complete": "Completed",
        "done": "Completed",
    }

    return status_map.get(value.lower(), value)


def normalize_priority(value: str | None) -> str:
    value = normalize_text(value)

    if not value:
        return "Medium"

    priority_map = {
        "low": "Low",
        "medium": "Medium",
        "med": "Medium",
        "high": "High",
        "critical": "Critical",
    }

    return priority_map.get(value.lower(), value)


def normalize_date(
    value: str | float | int | date | datetime | None,
) -> date | None:
    if value is None:
        return None

    if pd.isna(value):
        return None

    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    value = str(value).strip()

    if not value:
        return None

    supported_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%m-%d-%Y",
    ]

    for date_format in supported_formats:
        try:
            return datetime.strptime(
                value,
                date_format,
            ).date()
        except ValueError:
            continue

    raise ValueError(
        f"Invalid date '{value}'. "
        "Supported formats: YYYY-MM-DD, MM/DD/YYYY, MM-DD-YYYY."
    )


def normalize_hours(value: str | None) -> float | None:
    value = normalize_text(value)

    if not value:
        return None

    try:
        hours = float(value)
    except ValueError as exc:
        raise ValueError(
            f"Invalid hours value '{value}'."
        ) from exc

    if hours < 0:
        raise ValueError(
            f"Hours cannot be negative: '{value}'."
        )

    return hours


def parse_csv(content: bytes) -> list[ImportTask]:
    text = content.decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(text))

    if not reader.fieldnames:
        raise ValueError("CSV file does not contain a header row.")

    reader.fieldnames = [
        normalize_column_name(column)
        for column in reader.fieldnames
        if column
    ]

    missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    tasks = []

    for row_number, row in enumerate(reader, start=2):
        try:
            task = ImportTask(
                project_name=normalize_text(
                    row.get("project_name")
                ),
                project_description=normalize_text(
                    row.get("project_description")
                ),
                project_status=normalize_status(
                    row.get("project_status")
                ),
                task_name=normalize_text(
                    row.get("task_name")
                ),
                task_description=normalize_text(
                    row.get("task_description")
                ),
                task_status=normalize_status(
                    row.get("task_status")
                ),
                task_priority=normalize_priority(
                    row.get("task_priority")
                ),
                due_date=normalize_date(
                    row.get("due_date")
                ),
                estimated_hours=normalize_hours(
                    row.get("estimated_hours")
                ),
                actual_hours=normalize_hours(
                    row.get("actual_hours")
                ),
            )

            tasks.append(task)

        except Exception as exc:
            raise ValueError(
                f"Invalid data on CSV row {row_number}: {exc}"
            ) from exc

    return tasks


def parse_excel(content: bytes) -> list[ImportTask]:
    dataframe = pd.read_excel(
        io.BytesIO(content)
    )

    if dataframe.empty:
        raise ValueError(
            "Excel file contains no data rows."
        )

    dataframe.columns = [
        normalize_column_name(str(column))
        for column in dataframe.columns
        if column is not None
    ]

    missing_columns = (
        REQUIRED_COLUMNS
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    tasks = []

    for row_number, row in enumerate(
        dataframe.to_dict(orient="records"),
        start=2,
    ):
        try:
            task = ImportTask(
                project_name=normalize_text(
                    row.get("project_name")
                ),
                project_description=normalize_text(
                    row.get("project_description")
                ),
                project_status=normalize_status(
                    row.get("project_status")
                ),
                task_name=normalize_text(
                    row.get("task_name")
                ),
                task_description=normalize_text(
                    row.get("task_description")
                ),
                task_status=normalize_status(
                    row.get("task_status")
                ),
                task_priority=normalize_priority(
                    row.get("task_priority")
                ),
                due_date=normalize_date(
                    row.get("due_date")
                ),
                estimated_hours=normalize_hours(
                    row.get("estimated_hours")
                ),
                actual_hours=normalize_hours(
                    row.get("actual_hours")
                ),
            )

            tasks.append(task)

        except Exception as exc:
            raise ValueError(
                f"Invalid data on Excel row {row_number}: {exc}"
            ) from exc

    return tasks


def parse_import_file(
    content: bytes,
    filename: str,
) -> list[ImportTask]:
    filename = filename.lower()

    if filename.endswith(".csv"):
        return parse_csv(content)

    if filename.endswith(".xlsx"):
        return parse_excel(content)

    if filename.endswith(".xls"):
        return parse_excel(content)

    raise ValueError(
        "Unsupported file type. "
        "Supported formats: CSV, XLS, XLSX."
    )