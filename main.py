from datetime import datetime, timedelta, date
from pathlib import Path

# --- Habit Engine imports ---
from habit_engine.domain.habit import Habit
from habit_engine.services.analytics_service import HabitAnalyticsService
from habit_engine.services.recommendation_service import HabitRecommendationService
from habit_engine.services.habit_service import HabitService
from habit_engine.persistence.in_memory_repository import InMemoryHabitRepository

# --- Task Engine imports ---
from task_engine.domain.task import Task, Priority
from task_engine.services.scheduling_service import SchedulingService
from task_engine.algorithms.priority_scheduler import PriorityScheduler

# --- Habit-Task Bridge ---
from integration.habit_task_bridge import HabitTaskBridge

# --- Code Analyzer ---
from code_analyzer.analyzer import CodeAnalyzer

# ---------------------------
# 1️⃣ Setup Habit Engine
# ---------------------------
habit_repo = InMemoryHabitRepository()
analytics_service = HabitAnalyticsService()
recommendation_service = HabitRecommendationService()
habit_service = HabitService(habit_repo, analytics_service, recommendation_service)

# Sample habits
habits = [
    Habit(1, "Exercise", 3, date.today() - timedelta(days=10), [date.today() - timedelta(days=1)]),
    Habit(2, "Reading", 2, date.today() - timedelta(days=7), [])
]

for h in habits:
    habit_repo.add(h)

# ---------------------------
# 2️⃣ Setup Task Engine
# ---------------------------
tasks = [
    Task(1, "Finish report", Priority.MEDIUM, 60, datetime.now() + timedelta(hours=2)),
    Task(2, "Email client", Priority.LOW, 30, datetime.now() + timedelta(hours=1)),
    Task(3, "Prepare slides", Priority.HIGH, 90, datetime.now() + timedelta(hours=4)),
]

# Habit-aware scheduling
bridge = HabitTaskBridge(analytics_service)
habit_aware_schedule = bridge.generate_habit_aware_schedule(tasks, habits)

print("\n=== Habit-Aware Task Schedule ===")
for t in habit_aware_schedule:
    print(f"{t.title} - Priority: {t.priority.name}")

# ---------------------------
# 3️⃣ Display Habit Analytics + Recommendations
# ---------------------------
print("\n=== Habit Analytics & Recommendations ===")
for h in habits:
    consistency = analytics_service.calculate_consistency(h)
    streak = analytics_service.current_streak(h)
    recs = recommendation_service.recommend(h)
    print(f"\nHabit: {h.name}")
    print(f"Consistency: {consistency:.2f}")
    print(f"Current Streak: {streak}")
    print("Recommendations:")
    for r in recs:
        print(f" - {r}")

# ---------------------------
# 4️⃣ Run Code Analyzer
# ---------------------------
print("\n=== Code Analyzer Report ===")
analyzer = CodeAnalyzer()
analyzer.analyze_directory(Path("habit_engine"))  # analyze own modules




# python main.py
