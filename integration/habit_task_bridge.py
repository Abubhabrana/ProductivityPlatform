from typing import List
from habit_engine.services.analytics_service import HabitAnalyticsService
from habit_engine.domain.habit import Habit
from task_engine.domain.task import Task, Priority
from task_engine.services.scheduling_service import SchedulingService
from task_engine.algorithms.priority_scheduler import PriorityScheduler

class HabitTaskBridge:
    """Adjusts task scheduling based on habit analytics."""

    def __init__(self, analytics_service: HabitAnalyticsService):
        self._analytics = analytics_service

    def adjust_priorities(self, tasks: List[Task], habits: List[Habit]) -> List[Task]:
        """
        Adjust task priorities based on habits.
        - Low consistency habits -> critical tasks earlier
        - High consistency habits -> normal priority
        """
        habit_scores = [self._analytics.calculate_consistency(h) for h in habits]

        # Simple heuristic: average consistency
        if not habit_scores:
            avg_consistency = 1.0
        else:
            avg_consistency = sum(habit_scores) / len(habit_scores)

        adjusted_tasks = []

        for task in tasks:
            # Increase priority if habits are inconsistent
            if avg_consistency < 0.5 and task.priority != Priority.HIGH:
                task.priority = Priority(task.priority.value + 1)
            adjusted_tasks.append(task)

        return adjusted_tasks

    def generate_habit_aware_schedule(
        self, tasks: List[Task], habits: List[Habit]
    ) -> List[Task]:
        adjusted_tasks = self.adjust_priorities(tasks, habits)
        scheduler = SchedulingService(PriorityScheduler())
        schedule = scheduler.generate_schedule(adjusted_tasks)
        return schedule.tasks
