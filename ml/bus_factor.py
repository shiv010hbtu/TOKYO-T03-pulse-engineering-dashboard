from collections import defaultdict


def calculate_bus_factor(commits: list) -> dict:
    """
    Bus Factor = minimum number of contributors whose absence
    would significantly impact the project.

    Input: list of commits with 'author' and 'files' fields
    Output: bus factor score and analysis
    """

    if not commits:
        return {"bus_factor": 0, "risk": "Unknown", "analysis": "No data"}

    # Count files owned by each contributor
    file_ownership = defaultdict(set)
    contributor_commits = defaultdict(int)

    for commit in commits:
        author = commit.get("author", "unknown")
        files = commit.get("files", [])
        contributor_commits[author] += 1
        for file in files:
            file_ownership[author].add(file)

    total_files = len(set(f for files in file_ownership.values() for f in files))
    total_contributors = len(contributor_commits)

    if total_files == 0:
        return {
            "bus_factor": 1,
            "risk": "High",
            "analysis": "Unable to determine file ownership"
        }

    # Sort contributors by files owned
    sorted_contributors = sorted(
        file_ownership.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    # Find how many contributors own 50%+ of files
    cumulative = 0
    bus_factor = 0
    threshold = total_files * 0.5

    for contributor, files in sorted_contributors:
        cumulative += len(files)
        bus_factor += 1
        if cumulative >= threshold:
            break

    # Risk level
    if bus_factor == 1:
        risk = "Critical"
        analysis = f"Only 1 contributor owns majority of codebase. High single point of failure!"
    elif bus_factor == 2:
        risk = "High"
        analysis = f"Only {bus_factor} contributors own most of the code. Team is vulnerable."
    elif bus_factor <= 3:
        risk = "Medium"
        analysis = f"{bus_factor} key contributors. Moderate risk if any leave."
    else:
        risk = "Low"
        analysis = f"Knowledge is distributed across {bus_factor}+ contributors. Healthy!"

    return {
        "bus_factor": bus_factor,
        "risk": risk,
        "analysis": analysis,
        "total_contributors": total_contributors,
        "contributor_breakdown": {
            name: len(files) for name, files in sorted_contributors
        }
    }


if __name__ == "__main__":
    test_commits = [
        {"author": "Shivendra", "files": ["ml/classifier.py", "ml/scorer.py", "ml/summarizer.py"]},
        {"author": "Shivendra", "files": ["ml/bus_factor.py", "ml/health_score.py"]},
        {"author": "Alice", "files": ["backend/main.py", "backend/routes.py"]},
        {"author": "Bob", "files": ["frontend/App.js"]},
        {"author": "Alice", "files": ["backend/github_client.py"]},
    ]
    print("=== Bus Factor Test ===")
    result = calculate_bus_factor(test_commits)
    print(f"  Bus Factor: {result['bus_factor']}")
    print(f"  Risk: {result['risk']}")
    print(f"  Analysis: {result['analysis']}")
