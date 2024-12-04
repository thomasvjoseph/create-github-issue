import os
from github import Github

def main():
    try:
        # Extract inputs from environment variables
        title = os.getenv('INPUT_TITLE')
        token = os.getenv('GITHUB_TOKEN')
        labels = os.getenv('INPUT_LABELS', '').strip()
        assignees = os.getenv('INPUT_ASSIGNEES', '').strip()
        body = os.getenv('INPUT_BODY', '').strip()

        # Validate title
        if not title:
            raise ValueError("Issue title is required")

        # Process labels and assignees
        label_list = labels.split(',') if labels else []
        assignee_list = [a.strip() for a in assignees.split(',') if a.strip()] if assignees else []

        # Authenticate and create issue
        github = Github(token)
        repo = github.get_repo(os.getenv('GITHUB_REPOSITORY'))
        
        issue = repo.create_issue(
            title=title,
            body=body,
            labels=label_list,
            assignees=assignee_list
        )
        
        print(f"Issue created successfully: {issue.html_url}")
    
    except Exception as e:
        print(f"Error creating GitHub issue: {e}")
        raise

if __name__ == "__main__":
    main()