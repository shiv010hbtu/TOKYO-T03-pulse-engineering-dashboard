import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

CATEGORIES = ["Feature", "Bug Fix", "Refactor", "Docs", "Test", "Chore"]

def classify_commit(commit_message: str) -> dict:
    """
    Classifies a commit message into a category.
    Input: commit message string
    Output: dict with category and confidence
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = f"""
        Classify this git commit message into exactly one of these categories:
        {", ".join(CATEGORIES)}

        Commit message: "{commit_message}"

        Reply with ONLY the category name, nothing else.
        """
        response = model.generate_content(prompt)
        category = response.text.strip()

        if category not in CATEGORIES:
            category = rule_based_classify(commit_message)

        return {
            "message": commit_message,
            "category": category,
            "method": "llm"
        }

    except Exception as e:
        # Fallback to rule-based if API fails
        category = rule_based_classify(commit_message)
        return {
            "message": commit_message,
            "category": category,
            "method": "rule_based"
        }


def rule_based_classify(message: str) -> str:
    """Fallback: rule-based classification"""
    message = message.lower()
    if any(w in message for w in ["fix", "bug", "patch", "resolve", "error"]):
        return "Bug Fix"
    elif any(w in message for w in ["feat", "add", "new", "implement", "create"]):
        return "Feature"
    elif any(w in message for w in ["refactor", "clean", "improve", "restructure"]):
        return "Refactor"
    elif any(w in message for w in ["doc", "readme", "comment", "changelog"]):
        return "Docs"
    elif any(w in message for w in ["test", "spec", "coverage", "unit"]):
        return "Test"
    else:
        return "Chore"


def classify_multiple(commit_messages: list) -> list:
    """Classify multiple commits"""
    return [classify_commit(msg) for msg in commit_messages]


# Test karne ke liye
if __name__ == "__main__":
    test_commits = [
        "fix: resolve login timeout issue",
        "feat: add dashboard heatmap component",
        "docs: update README with setup instructions",
        "refactor: clean up auth module",
        "test: add unit tests for classifier"
    ]
    print("=== Commit Classification Test ===")
    for commit in test_commits:
        result = classify_commit(commit)
        print(f"  '{commit}' → {result['category']} ({result['method']})")
