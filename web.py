from flask import Flask, render_template, request, redirect, url_for
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

app = Flask(__name__)

# Global data setup (in a real app, this would be in a database)
habit_repo = InMemoryHabitRepository()
analytics_service = HabitAnalyticsService()
recommendation_service = HabitRecommendationService()
habit_service = HabitService(habit_repo, analytics_service, recommendation_service)

# Sample habits with higher completion rates for demonstration (over 7 days)
habits = [
    Habit(1, "Exercise", 3, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in [1,2,3,4,5,6,7]]),  # High consistency ~87.5%
    Habit(2, "Reading", 2, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in [1,2,3,4,5,6]]),  # High consistency ~85.7%
    Habit(3, "Meditation", 1, date.today() - timedelta(days=7), [date.today() - timedelta(days=3)]),  # Low but some consistency ~14.3%
    Habit(4, "Drink Water", 7, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in range(7)]),  # Perfect weekly habit ~100%
    Habit(5, "Code Practice", 5, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in [0,1,2,3,4,5,6]]),  # High consistency ~87.5%
    Habit(6, "Healthy Eating", 4, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in [1,2,3,4,5]]),  # High consistency ~71.4%
    Habit(7, "Sleep Early", 6, date.today() - timedelta(days=7),
          [date.today() - timedelta(days=i) for i in [1,2,3,4,5,6,7]]),  # Excellent streak ~100%
]

for h in habits:
    habit_repo.add(h)

# Sample tasks
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

@app.route('/')
def dashboard():
    # Habit-aware scheduling
    bridge = HabitTaskBridge(analytics_service)
    habit_aware_schedule = bridge.generate_habit_aware_schedule(tasks, habits)

    # Analytics data
    habit_data = []
    for h in habits:
        consistency = analytics_service.calculate_consistency(h)
        streak = analytics_service.current_streak(h)
        recs = recommendation_service.recommend(h)
        habit_data.append({
            'name': h.name,
            'consistency': round(consistency * 100, 2),
            'streak': streak,
            'recommendations': recs
        })

    return render_template('dashboard.html',
                         tasks=habit_aware_schedule,
                         habits=habit_data)

@app.route('/habits')
def habits_page():
    habit_data = []
    for h in habits:
        consistency = analytics_service.calculate_consistency(h)
        streak = analytics_service.current_streak(h)
        recs = recommendation_service.recommend(h)
        habit_data.append({
            'name': h.name,
            'consistency': round(consistency * 100, 2),
            'streak': streak,
            'recommendations': recs
        })
    return render_template('habits.html', habits=habit_data)

@app.route('/tasks')
def tasks_page():
    bridge = HabitTaskBridge(analytics_service)
    habit_aware_schedule = bridge.generate_habit_aware_schedule(tasks, habits)
    return render_template('tasks.html', tasks=habit_aware_schedule)

@app.route('/code-analysis')
def code_analysis():
    analyzer = CodeAnalyzer()
    analyzer_results = {}
    for file_path, tree in analyzer.parser.parse_directory(Path("habit_engine")):
        issues = []
        for rule in analyzer.rules:
            issues.extend(rule.analyze(tree))
        analyzer_results[file_path] = issues
    return render_template('code_analysis.html', results=analyzer_results)

@app.route('/generate-report')
def generate_report():
    bridge = HabitTaskBridge(analytics_service)
    habit_aware_schedule = bridge.generate_habit_aware_schedule(tasks, habits)

    analyzer = CodeAnalyzer()
    analyzer_results = {}
    for file_path, tree in analyzer.parser.parse_directory(Path("habit_engine")):
        issues = []
        for rule in analyzer.rules:
            issues.extend(rule.analyze(tree))
        analyzer_results[file_path] = issues

    report_gen = ReportGenerator("productivity_report.md")
    analytics_service.recommendation_service = recommendation_service
    report_gen.write_report(habit_aware_schedule, habits, analytics_service, analyzer_results)

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
