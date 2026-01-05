from pathlib import Path
from typing import List
from task_engine.domain.task import Task
from habit_engine.domain.habit import Habit

class ReportGenerator:
    """Generates a full project report including tasks, habits, and analyzer results in Markdown."""

    def __init__(self, output_file: str = "productivity_report.md"):
        self.output_file = Path(output_file)

    def write_report(
        self,
        tasks: List[Task],
        habits: List[Habit],
        analytics_service,
        analyzer_results: dict
    ):
        with self.output_file.open("w", encoding="utf-8") as f:
            # -------------------
            # Habit-Aware Task Schedule
            # -------------------
            f.write("# 🗓 Habit-Aware Task Schedule\n\n")
            if tasks:
                f.write("| Task | Priority | Duration (min) |\n")
                f.write("|------|---------|----------------|\n")
                for t in tasks:
                    # Only use attributes we know exist
                    duration = getattr(t, "duration", "N/A")
                    priority = getattr(t, "priority", "N/A")
                    f.write(f"| {t.title} | {priority} | {duration} |\n")
            else:
                f.write("No tasks scheduled.\n")

            # -------------------
            # Habit Analytics & Recommendations
            # -------------------
            f.write("\n# 📊 Habit Analytics & Recommendations\n\n")
            for h in habits:
                consistency = analytics_service.calculate_consistency(h)
                streak = analytics_service.current_streak(h)
                f.write(f"## Habit: **{h.name}**\n")
                f.write(f"- **Consistency:** {consistency:.2f}\n")
                f.write(f"- **Current Streak:** {streak} days\n")
                f.write("- **Recommendations:**\n")

                recs = []
                if hasattr(analytics_service, "recommendation_service"):
                    recs = analytics_service.recommendation_service.recommend(h)
                if not recs:
                    if consistency < 0.5:
                        recs = ["Your consistency is moderate, keep building momentum!"]
                    else:
                        recs = ["Keep going! You're doing well."]
                for r in recs:
                    f.write(f"  - {r}\n")

            # -------------------
            # Code Analyzer Report
            # -------------------
            f.write("\n# 🖥 Code Analyzer Report\n\n")
            for file_path, issues in analyzer_results.items():
                f.write(f"## File: `{file_path}`\n")
                if not issues:
                    f.write("✅ No issues found.\n\n")
                else:
                    f.write("⚠️ Issues:\n")
                    f.write("```\n")
                    for issue in issues:
                        f.write(f"{issue}\n")
                    f.write("```\n\n")

        print(f"\n✅ Markdown report generated at: {self.output_file.resolve()}")
