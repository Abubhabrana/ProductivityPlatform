from habit_engine.persistence.habit_repository import HabitRepository
from habit_engine.domain.habit import Habit
from typing import List, Optional


class InMemoryHabitRepository(HabitRepository):
    """Simple in-memory habit repository for testing/demo purposes."""

    def __init__(self):
        self._habits: List[Habit] = []

    def add(self, habit: Habit) -> None:
        self._habits.append(habit)

    def get_by_id(self, habit_id: int) -> Optional[Habit]:
        for h in self._habits:
            if h.id == habit_id:
                return h
        return None

    def list_all(self) -> List[Habit]:
        return self._habits.copy()
