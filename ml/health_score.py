from collections import defaultdict
from datetime import datetime, timezone


def calculate_health_score(commits: list, contributors: list) -> dict:
    """
    Overall engineering health score (0-100).
    Based on: commit frequency, contributor diversity, bug ratio, recency
    """

    if not commits:
        return {"health_score": 0, "grade": "F", "breakdown": {}}

    total_commits = len(commits)
    total_contributors = len(contributors)

    # 1. Contributor Diversity Score (25 pts)
    if total_contributors >= 4:
        diversity_score = 25
    elif total_contributors == 3:
        diversity_score = 20
    elif total_contributors == 2:
        diversity_score = 12
    else:
        diversity_score = 5

    # 2. Commit Frequency Score (25 pts)
    if total_commits >= 50:
        frequency_score = 25
    elif total_commits >= 30:
        frequency_score = 20
    elif total_commits >= 15:
        frequency_score = 15
    elif total_commits >= 5:
        frequency_score = 10
    else:
        frequency_score = 5

    # 3. Bug Ratio Score (25 pts) — fewer bugs = better
    bug_commits = sum(
        1 for c in commits
        if any(w in c.get("message", "").lower() for w in ["fix", "bug", "patch", "error", "resolve"])
    )
    bug_ratio = bug_commits / total_commits if total_commits > 0 else 0

    if bug_ratio < 0.1:
        bug_score = 25
    elif bug_ratio < 0.2:
        bug_score = 20
    elif bug_ratio < 0.35:
        bug_score = 15
    elif bug_ratio < 0.5:
        bug_score = 10
    else:
        bug_score = 5

    # 4. Commit Distribution Score (25 pts) — even distribution
    author_counts = defaultdict(int)
    for commit in commits:
        author_counts[commit.get("author", "unknown")] += 1

    if author_counts:
        max_commits = max(author_counts.values())
        dominance_ratio = max_commits / total_commits
        if dominance_ratio < 0.4:
            distribution_score = 25
        elif dominance_ratio < 0.6:
            distribution_score = 18
        elif dominance_ratio < 0.8:
            distribution_score = 10
        else:
            distribution_score = 5
    else:
        distribution_score = 0

    # Total
    total_score = diversity_score + frequency_score + bug_score + distribution_score

    # Grade
    if total_score >= 85:
        grade = "A"
    elif total_score >= 70:
        grade = "B"
    elif total_score >= 55:
        grade = "C"
    elif total_score >= 40:
        grade = "D"
    else:
        grade = "F"

    return {
        "health_score": total_score,
        "grade": grade,
        "breakdown": {
            "contributor_diversity": diversity_score,
            "commit_frequency": frequency_score,
            "bug_ratio": bug_score,
            "commit_distribution": distribution_score
        },
        "stats": {
            "total_commits": total_commits,
            "total_contributors": total_contributors,
            "bug_ratio_percent": round(bug_ratio * 100, 1)
        }
    }


if __name__ == "__main__":
    test_commits = [
        {"author": "Shivendra", "message": "feat: add classifier"},
        {"author": "Alice", "message": "fix: resolve API timeout"},
        {"author": "Bob", "message": "feat: add dashboard"},
        {"author": "Shivendra", "message": "docs: update README"},
        {"author": "Alice", "message": "test: add unit tests"},
        {"author": "Charlie", "message": "refactor: clean auth module"},
    ]
    print("=== Health Score Test ===")
    result = calculate_health_score(test_commits, ["Shivendra", "Alice", "Bob", "Charlie"])
    print(f"  Health Score: {result['health_score']}/100")
    print(f"  Grade: {result['grade']}")
    print(f"  Breakdown: {result['breakdown']}")
