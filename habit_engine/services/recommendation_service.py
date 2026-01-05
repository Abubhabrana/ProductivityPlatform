from datetime import date, timedelta
from habit_engine.domain.habit import Habit


class HabitRecommendationService:
    """Generates behavior-based recommendations for habits."""

    def recommend(self, habit: Habit) -> list[str]:
        recommendations: list[str] = []

        if not habit.completions:
            recommendations.append(
                "Start small: aim to complete this habit at least once this week."
            )
            return recommendations

        days_active = (date.today() - habit.start_date).days + 1
        expected_completions = (days_active / 7) * habit.frequency_per_week
        actual_completions = len(set(habit.completions))

        consistency_ratio = actual_completions / max(expected_completions, 1)

        if consistency_ratio < 0.5:
            recommendations.append(
                "Your consistency is low. Consider reducing the weekly frequency."
            )

        if consistency_ratio >= 1.0:
            recommendations.append(
                "Great consistency! You may increase difficulty or frequency."
            )

        recent_cutoff = date.today() - timedelta(days=7)
        recent_activity = [
            d for d in habit.completions if d >= recent_cutoff
        ]

        if not recent_activity:
            recommendations.append(
                "No activity in the last week. Try changing the time or context."
            )

        return recommendations
