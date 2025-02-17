import argparse
import json
import os

from jira import JIRA

parser = argparse.ArgumentParser(description='Sync Jira actions')
parser.add_argument('--cron-job', required=False, default=False)
parser.add_argument('--jira-project', required=True)
parser.add_argument('--perform-action', required=False)
parser.add_argument('--issue-numbers', required=False, default=[])


def connect_to_jira():
    # Only with token, token in raw format, without any prefix, in secrets as JIRA_TOKEN
    print('Connecting to Jira Server ...')
    return JIRA(os.environ['JIRA_URL'], token_auth=os.environ['JIRA_TOKEN'])


def main(args):
    args = parser.parse_args()
    print(f'Cron job from argument: {args.cron_job}')
    print(f'Jira project from argument: {args.jira_project}')
    print(f'Perform action from argument: {args.perform_action}')
    print(f'Issue numbers from argument: {args.issue_numbers}')

    # Check if running in GitHub action context
    if not os.getenv('GITHUB_ACTIONS'):
        raise SystemExit('Not running in GitHub action context, nothing to do ...')  # FIXME: handle this better-testing

    # Connect to Jira server
    jira = connect_to_jira()
    print(f'Jira user: {jira.myself()["name"]}')  # DEVTEST: Smoke test - print Jira user

    # Set event name
    event_name = os.environ.get('GITHUB_EVENT_NAME')

    # Load event data
    with open(os.environ.get('GITHUB_EVENT_PATH'), encoding='utf-8') as f:
        event = json.load(f)

    # Determine action from the event payload
    action = event.get('action')

    # Use match-case for handling different events
    match (event_name, action):
        case ('pull_request', 'opened'):
            print('A pull request was created in the repo.')
        case ('issues', 'opened'):
            print('An issue was created in the repo.')
        case ('issue_comment', 'created') if 'pull_request' in event.get('issue', {}):
            print('A comment was created on a pull request.')
        case ('issue_comment', 'created'):
            print('A comment was created on an issue.')
        case _:
            raise SystemExit(f'Unhandled event: {event_name} with action: {action}')


if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
