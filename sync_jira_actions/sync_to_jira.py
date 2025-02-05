import os
import argparse

parser = argparse.ArgumentParser(description="Sync Jira actions")
parser.add_argument("--cron-job", required=False, default=False)
parser.add_argument("--jira-project", required=True)
parser.add_argument("--perform-action", required=True)
parser.add_argument("--issue-numbers", required=False, default=[])


def main(args):
    args = parser.parse_args()
    print(f"Cron job from argument: {args.cron_job}")
    print(f"Jira project from argument: {args.jira_project}")
    print(f"Perform action from argument: {args.perform_action}")
    print(f"Issue numbers from argument: {args.issue_numbers}")

    # Check if running in GitHub action context
    if not os.getenv("GITHUB_ACTIONS"):
        print("❌ Not running in GitHub action context, nothing to do")
        raise SystemExit(0)


if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
