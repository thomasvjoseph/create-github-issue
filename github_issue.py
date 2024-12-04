import os
import time
from datetime import datetime, timedelta
import requests

# Environment variables provided by GitHub Actions
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
RUN_ID = os.getenv("GITHUB_RUN_ID")
REPO = os.getenv("GITHUB_REPOSITORY")
TIMEOUT_MINUTES = int(os.getenv("TIMEOUT_MINUTES", 10))  # Default timeout of 10 minutes

HEADERS = {"Authorization": f"Bearer {GITHUB_TOKEN}"}

def get_workflow_comments():
    """Fetch comments from the workflow run's issue-like discussion."""
    url = f"https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}/comments"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch comments: {response.status_code}, {response.text}")
        return []

def wait_for_approval(timeout_minutes):
    """Wait for 'yes' or 'approved' within the timeout period."""
    print(f"Waiting for manual approval (timeout: {timeout_minutes} minutes)...")
    timeout_time = datetime.now() + timedelta(minutes=timeout_minutes)

    while datetime.now() < timeout_time:
        comments = get_workflow_comments()
        for comment in comments:
            body = comment["body"].strip().lower()
            if body in ["yes", "approved"]:
                print(f"Approval received from {comment['user']['login']}!")
                return True
            elif body in ["no", "denied"]:
                print(f"Workflow denied by {comment['user']['login']}.")
                return False

        print("No response yet. Checking again in 30 seconds...")
        time.sleep(30)

    print("Timeout reached. Denying the workflow by default.")
    return False

if __name__ == "__main__":
    if wait_for_approval(TIMEOUT_MINUTES):
        print("Workflow approved. Proceeding...")
    else:
        print("Workflow denied or timed out.")
        exit(1)