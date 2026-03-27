def calculate_impact_score(
    lines_added: int,
    lines_deleted: int,
    files_changed: int,
    category: str
) -> dict:
    """
    Calculate impact score for a commit (1-10).
    Based on: lines changed, files affected, commit type
    """

    # Category weights
    category_weight = {
        "Feature": 1.5,
        "Bug Fix": 1.3,
        "Refactor": 1.1,
        "Test": 1.0,
        "Docs": 0.7,
        "Chore": 0.5
    }

    total_lines = lines_added + lines_deleted

    # Base score from lines changed (max 5 points)
    if total_lines == 0:
        line_score = 0
    elif total_lines < 10:
        line_score = 1
    elif total_lines < 50:
        line_score = 2
    elif total_lines < 150:
        line_score = 3
    elif total_lines < 500:
        line_score = 4
    else:
        line_score = 5

    # Files score (max 3 points)
    if files_changed == 0:
        file_score = 0
    elif files_changed <= 2:
        file_score = 1
    elif files_changed <= 5:
        file_score = 2
    else:
        file_score = 3

    # Base score (max 8)
    base_score = line_score + file_score

    # Apply category weight
    weight = category_weight.get(category, 1.0)
    final_score = min(10, round(base_score * weight, 1))

    return {
        "impact_score": final_score,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "files_changed": files_changed,
        "category": category,
        "breakdown": {
            "line_score": line_score,
            "file_score": file_score,
            "category_weight": weight
        }
    }


# Test
if __name__ == "__main__":
    print("=== Impact Score Test ===")
    tests = [
        (200, 50, 8, "Feature"),
        (5, 2, 1, "Bug Fix"),
        (0, 0, 1, "Docs"),
        (500, 300, 20, "Refactor"),
    ]
    for la, ld, fc, cat in tests:
        result = calculate_impact_score(la, ld, fc, cat)
        print(f"  {cat} (+{la}/-{ld}, {fc} files) → Score: {result['impact_score']}/10")
