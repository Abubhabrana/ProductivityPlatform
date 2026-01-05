from habit_engine.persistence.habit_repository import HabitRepository
from habit_engine.services.analytics_service import HabitAnalyticsService
from habit_engine.services.recommendation_service import HabitRecommendationService


class HabitService:
    """Application service coordinating habit-related operations."""

    def __init__(
        self,
        repository: HabitRepository,
        analytics: HabitAnalyticsService,
        recommender: HabitRecommendationService,
    ) -> None:
        self._repository = repository
        self._analytics = analytics
        self._recommender = recommender

    def analyze_habit(self, habit_id: int) -> dict:
        habit = self._repository.get_by_id(habit_id)
        if not habit:
            raise ValueError("Habit not found")

        return {
            "consistency": self._analytics.calculate_consistency(habit),
            "current_streak": self._analytics.current_streak(habit),
            "recommendations": self._recommender.recommend(habit),
        }
