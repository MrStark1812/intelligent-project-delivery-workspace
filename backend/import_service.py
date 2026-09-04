import csv
import io

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
                project_name=row["project_name"].strip(),
                project_description=(
                    row.get("project_description") or None
                ),
                project_status=(
                    row.get("project_status") or "Not Started"
                ),
                task_name=row["task_name"].strip(),
                task_description=(
                    row.get("task_description") or None
                ),
                task_status=(
                    row.get("task_status") or "Not Started"
                ),
                task_priority=(
                    row.get("task_priority") or "Medium"
                ),
                due_date=(
                    row.get("due_date") or None
                ),
                estimated_hours=(
                    float(row["estimated_hours"])
                    if row.get("estimated_hours")
                    else None
                ),
                actual_hours=(
                    float(row["actual_hours"])
                    if row.get("actual_hours")
                    else None
                ),
            )

            tasks.append(task)

        except Exception as exc:
            raise ValueError(
                f"Invalid data on CSV row {row_number}: {exc}"
            ) from exc

    return tasks