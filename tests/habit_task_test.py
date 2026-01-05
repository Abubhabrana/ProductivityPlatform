from datetime import datetime, timedelta, date
from habit_engine.domain.habit import Habit
from habit_engine.services.analytics_service import HabitAnalyticsService
from integration.habit_task_bridge import HabitTaskBridge
from task_engine.domain.task import Task, Priority

# Example habits
habits = [
    Habit(1, "Exercise", 3, date.today() - timedelta(days=10), [date.today() - timedelta(days=1)]),
    Habit(2, "Reading", 2, date.today() - timedelta(days=7), [])
]

# Example tasks
tasks = [
    Task(1, "Finish report", Priority.MEDIUM, 60, datetime.now() + timedelta(hours=2)),
    Task(2, "Email client", Priority.LOW, 30, datetime.now() + timedelta(hours=1)),
]

analytics = HabitAnalyticsService()
bridge = HabitTaskBridge(analytics)

scheduled_tasks = bridge.generate_habit_aware_schedule(tasks, habits)

print("Habit-aware schedule order:")
for t in scheduled_tasks:
    print(f"{t.title} - Priority: {t.priority.name}")

# $ python -m tests.habit_task_test