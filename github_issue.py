import os
from github import Github

# Extracting all the input from environment variables
title = os.getenv('INPUT_TITLE')  # Ensure this matches the input name in `action.yml`
token = os.getenv('GITHUB_TOKEN')  # Token automatically provided by GitHub Actions
labels = os.getenv('INPUT_LABELS')
assignees = os.getenv('INPUT_ASSIGNEES')
body = os.getenv('INPUT_BODY')

if not title:
    raise ValueError("Title is missing. Please provide a valid title for the issue.")

# If labels are provided, split by ',' to make it a list
if labels:
    labels = [label.strip() for label in labels.split(',') if label.strip()]
else:
    labels = []

# Validate and filter assignees
if assignees:
    assignees = [assignee.strip() for assignee in assignees.split(',') if assignee.strip()]
else:
    assignees = []

# Use the GitHub token to authenticate
github = Github(token)
repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))  # Format: "owner/repo"

# Create the issue
try:
    issue = repo.create_issue(
        title=title,
        body=body,
        assignees=assignees,
        labels=labels
    )
    print(f"Issue created successfully: {issue.html_url}")
except Exception as e:
    print(f"Error creating issue: {e}")
    raise

print("Environment Variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")