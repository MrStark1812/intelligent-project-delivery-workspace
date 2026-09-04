from datetime import date, timedelta

from database import Base, SessionLocal, engine
from models import Project, Task


projects = [
    {
        "name": "Customer Mobile Ordering Launch",
        "description": "Launch a mobile ordering experience for a major restaurant customer.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "Requirements Validation",
                "description": "Validate ordering, menu, and customer requirements.",
                "status": "Completed",
                "priority": "High",
                "due_date": date(2026, 8, 28),
                "estimated_hours": 12,
                "actual_hours": 10,
            },
            {
                "name": "Menu API Integration",
                "description": "Integrate restaurant menu data with the ordering platform.",
                "status": "Completed",
                "priority": "High",
                "due_date": date(2026, 9, 2),
                "estimated_hours": 20,
                "actual_hours": 18,
            },
            {
                "name": "Mobile Checkout",
                "description": "Implement and validate the mobile checkout experience.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 12),
                "estimated_hours": 24,
                "actual_hours": 12,
            },
            {
                "name": "Production Readiness",
                "description": "Complete production readiness and deployment validation.",
                "status": "Not Started",
                "priority": "Medium",
                "due_date": date(2026, 9, 18),
                "estimated_hours": 16,
                "actual_hours": None,
            },
        ],
    },
    {
        "name": "Digital Menu Integration",
        "description": "Integrate a customer's digital menu platform with the ordering experience.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "Menu Data Mapping",
                "description": "Map customer menu fields to the platform data model.",
                "status": "Completed",
                "priority": "Medium",
                "due_date": date(2026, 8, 30),
                "estimated_hours": 10,
                "actual_hours": 11,
            },
            {
                "name": "Menu Synchronization",
                "description": "Implement recurring synchronization between systems.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 5),
                "estimated_hours": 18,
                "actual_hours": 20,
            },
            {
                "name": "Error Handling",
                "description": "Implement handling for invalid and incomplete menu data.",
                "status": "Not Started",
                "priority": "Medium",
                "due_date": date(2026, 9, 10),
                "estimated_hours": 12,
                "actual_hours": None,
            },
            {
                "name": "Customer Validation",
                "description": "Complete customer validation of the integrated menu.",
                "status": "Not Started",
                "priority": "Medium",
                "due_date": date(2026, 9, 16),
                "estimated_hours": 8,
                "actual_hours": None,
            },
        ],
    },
    {
        "name": "Payment Gateway Rollout",
        "description": "Deploy a new payment gateway integration for restaurant ordering.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "Gateway Configuration",
                "description": "Configure payment gateway credentials and environments.",
                "status": "Completed",
                "priority": "High",
                "due_date": date(2026, 8, 25),
                "estimated_hours": 12,
                "actual_hours": 18,
            },
            {
                "name": "Payment API Integration",
                "description": "Integrate payment authorization and transaction APIs.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 8, 31),
                "estimated_hours": 20,
                "actual_hours": 32,
            },
            {
                "name": "Refund Processing",
                "description": "Implement refund and transaction reversal workflows.",
                "status": "Not Started",
                "priority": "High",
                "due_date": date(2026, 9, 7),
                "estimated_hours": 16,
                "actual_hours": None,
            },
            {
                "name": "Production Certification",
                "description": "Complete gateway certification and production readiness.",
                "status": "Not Started",
                "priority": "High",
                "due_date": date(2026, 9, 10),
                "estimated_hours": 20,
                "actual_hours": None,
            },
        ],
    },
    {
        "name": "Loyalty Platform Integration",
        "description": "Connect restaurant loyalty accounts and rewards with digital ordering.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "Loyalty Requirements",
                "description": "Document loyalty account and rewards requirements.",
                "status": "Completed",
                "priority": "Medium",
                "due_date": date(2026, 9, 4),
                "estimated_hours": 8,
                "actual_hours": 7,
            },
            {
                "name": "Customer Authentication",
                "description": "Integrate customer authentication with loyalty accounts.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 14),
                "estimated_hours": 18,
                "actual_hours": 10,
            },
            {
                "name": "Rewards Redemption",
                "description": "Implement redemption of loyalty rewards during checkout.",
                "status": "Not Started",
                "priority": "High",
                "due_date": date(2026, 9, 20),
                "estimated_hours": 20,
                "actual_hours": None,
            },
        ],
    },
    {
        "name": "POS Integration Upgrade",
        "description": "Upgrade the point-of-sale integration for a restaurant customer.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "POS Compatibility Review",
                "description": "Review compatibility between the current POS and integration layer.",
                "status": "Completed",
                "priority": "Medium",
                "due_date": date(2026, 8, 27),
                "estimated_hours": 12,
                "actual_hours": 19,
            },
            {
                "name": "Integration Development",
                "description": "Update integration services for the new POS version.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 3),
                "estimated_hours": 24,
                "actual_hours": 31,
            },
            {
                "name": "Regression Testing",
                "description": "Run regression testing across ordering and payment workflows.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 9),
                "estimated_hours": 20,
                "actual_hours": 8,
            },
            {
                "name": "Customer Sign-off",
                "description": "Obtain customer approval for production deployment.",
                "status": "Not Started",
                "priority": "Medium",
                "due_date": date(2026, 9, 15),
                "estimated_hours": 8,
                "actual_hours": None,
            },
        ],
    },
    {
        "name": "Multi-Location Restaurant Rollout",
        "description": "Roll out digital ordering capabilities across multiple restaurant locations.",
        "status": "In Progress",
        "tasks": [
            {
                "name": "Location Configuration",
                "description": "Configure restaurant locations and operational settings.",
                "status": "Completed",
                "priority": "High",
                "due_date": date(2026, 8, 24),
                "estimated_hours": 20,
                "actual_hours": 28,
            },
            {
                "name": "Menu Deployment",
                "description": "Deploy location-specific menus across all participating restaurants.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 8, 30),
                "estimated_hours": 30,
                "actual_hours": 42,
            },
            {
                "name": "Order Flow Validation",
                "description": "Validate ordering workflows across all locations.",
                "status": "In Progress",
                "priority": "High",
                "due_date": date(2026, 9, 4),
                "estimated_hours": 24,
                "actual_hours": 26,
            },
            {
                "name": "Production Rollout",
                "description": "Complete production rollout across all restaurant locations.",
                "status": "Not Started",
                "priority": "High",
                "due_date": date(2026, 9, 8),
                "estimated_hours": 32,
                "actual_hours": None,
            },
            {
                "name": "Post-Launch Validation",
                "description": "Validate production performance and customer acceptance.",
                "status": "Not Started",
                "priority": "Medium",
                "due_date": date(2026, 9, 12),
                "estimated_hours": 16,
                "actual_hours": None,
            },
        ],
    },
]


def seed_demo_data():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        for project_data in projects:
            project = Project(
                name=project_data["name"],
                description=project_data["description"],
                status=project_data["status"],
            )

            db.add(project)
            db.flush()

            for task_data in project_data["tasks"]:
                task = Task(
                    project_id=project.id,
                    name=task_data["name"],
                    description=task_data["description"],
                    status=task_data["status"],
                    priority=task_data["priority"],
                    due_date=task_data["due_date"],
                    estimated_hours=task_data["estimated_hours"],
                    actual_hours=task_data["actual_hours"],
                )

                db.add(task)

        db.commit()

        print(
            f"Seeded {len(projects)} demo projects "
            "with realistic task data."
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()