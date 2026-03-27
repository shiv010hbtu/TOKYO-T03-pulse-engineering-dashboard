import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def generate_contributor_summary(contributor_name: str, commits: list) -> dict:
    """
    Generate LLM-based summary of a contributor's activity.
    Input: name + list of commit messages
    Output: human-readable summary
    """
    if not commits:
        return {
            "contributor": contributor_name,
            "summary": "No commits found for this contributor.",
            "total_commits": 0
        }

    commit_text = "\n".join([f"- {c}" for c in commits[:30]])  # max 30 commits

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Analyze these git commits by '{contributor_name}' and write a 2-3 sentence
        professional summary of their contributions. Focus on what they worked on,
        their primary areas, and patterns.

        Commits:
        {commit_text}

        Write a concise, professional summary:
        """
        response = model.generate_content(prompt)
        summary = response.text.strip()

    except Exception as e:
        summary = f"{contributor_name} made {len(commits)} commits covering various aspects of the project."

    return {
        "contributor": contributor_name,
        "summary": summary,
        "total_commits": len(commits)
    }


def generate_repo_summary(repo_url: str, all_commits: list, contributors: list) -> dict:
    """Generate overall repository health summary"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Given this GitHub repository analysis:
        - Repository: {repo_url}
        - Total commits: {len(all_commits)}
        - Total contributors: {len(contributors)}
        - Recent commits: {all_commits[:10]}

        Write a 3-4 sentence engineering summary covering:
        1. Overall activity level
        2. Team collaboration
        3. Code health observations
        """
        response = model.generate_content(prompt)
        return {
            "repo": repo_url,
            "summary": response.text.strip(),
            "total_commits": len(all_commits),
            "total_contributors": len(contributors)
        }
    except Exception as e:
        return {
            "repo": repo_url,
            "summary": f"Repository with {len(all_commits)} commits by {len(contributors)} contributors.",
            "total_commits": len(all_commits),
            "total_contributors": len(contributors)
        }


if __name__ == "__main__":
    test_commits = [
        "feat: add login page",
        "fix: resolve JWT token expiry bug",
        "feat: implement dashboard charts",
        "test: add auth unit tests",
        "fix: fix mobile responsive layout"
    ]
    print("=== Contributor Summary Test ===")
    result = generate_contributor_summary("Shivendra", test_commits)
    print(f"  Contributor: {result['contributor']}")
    print(f"  Summary: {result['summary']}")
