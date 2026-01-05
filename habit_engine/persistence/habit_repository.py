from abc import ABC, abstractmethod
from habit_engine.domain.habit import Habit
from typing import List, Optional


class HabitRepository(ABC):
    """Abstract repository for habits."""

    @abstractmethod
    def add(self, habit: Habit) -> None:
        pass

    @abstractmethod
    def get_by_id(self, habit_id: int) -> Optional[Habit]:
        pass

    @abstractmethod
    def list_all(self) -> List[Habit]:
        pass
