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

# --- Report Generator ---
from integration.report_generator import ReportGenerator

# ---------------------------
# 1️⃣ Setup Habit Engine
# ---------------------------
habit_repo = InMemoryHabitRepository()
analytics_service = HabitAnalyticsService()
recommendation_service = HabitRecommendationService()
habit_service = HabitService(habit_repo, analytics_service, recommendation_service)

# Sample habits with different patterns
habits = [
    Habit(1, "Exercise", 3, date.today() - timedelta(days=15), 
          [date.today() - timedelta(days=i) for i in [1,3,4,5]]),
    Habit(2, "Reading", 2, date.today() - timedelta(days=10), 
          [date.today() - timedelta(days=i) for i in [2,5]]),
    Habit(3, "Meditation", 1, date.today() - timedelta(days=20), []),
    Habit(4, "Drink Water", 7, date.today() - timedelta(days=7), 
          [date.today() - timedelta(days=i) for i in range(5)]),
    Habit(5, "Code Practice", 5, date.today() - timedelta(days=12), 
          [date.today() - timedelta(days=i) for i in [0,1,2,4,5,7]]),
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
    Task(4, "Team meeting", Priority.HIGH, 45, datetime.now() + timedelta(hours=3)),
    Task(5, "Update project plan", Priority.MEDIUM, 50, datetime.now() + timedelta(hours=5)),
    Task(6, "Clean workspace", Priority.LOW, 20, datetime.now() + timedelta(hours=6)),
    Task(7, "Call supplier", Priority.MEDIUM, 30, datetime.now() + timedelta(hours=2, minutes=30)),
    Task(8, "Design review", Priority.HIGH, 120, datetime.now() + timedelta(hours=7)),
    Task(9, "Write documentation", Priority.MEDIUM, 90, datetime.now() + timedelta(hours=8)),
]

# Habit-aware scheduling
bridge = HabitTaskBridge(analytics_service)
habit_aware_schedule = bridge.generate_habit_aware_schedule(tasks, habits)

# ---------------------------
# 3️⃣ Run Code Analyzer
# ---------------------------
analyzer = CodeAnalyzer()
analyzer_results = {}
for file_path, tree in analyzer.parser.parse_directory(Path("habit_engine")):
    issues = []
    for rule in analyzer.rules:
        issues.extend(rule.analyze(tree))
    analyzer_results[file_path] = issues

# ---------------------------
# 4️⃣ Generate Markdown Report
# ---------------------------
report_gen = ReportGenerator("productivity_report.md")
analytics_service.recommendation_service = recommendation_service
report_gen.write_report(habit_aware_schedule, habits, analytics_service, analyzer_results)

# ---------------------------
# 5️⃣ Console Output for Presentation
# ---------------------------
print("\n=== Habit-Aware Task Schedule ===")
for t in habit_aware_schedule:
    print(f"{t.title} - Priority: {t.priority.name}")

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

print("\n=== Code Analyzer Report ===")
for file_path, issues in analyzer_results.items():
    print(f"\nFile: {file_path}")
    if not issues:
        print("  No issues found ✅")
    else:
        for issue in issues:
            print(f"  ⚠️ {issue}")

print(f"\n✅ Full Markdown report saved to 'productivity_report.md'")
