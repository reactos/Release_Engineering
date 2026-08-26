#
# PROJECT:     ReactOS Release Document Scripts
# LICENSE:     MIT (https://spdx.org/licenses/MIT)
# PURPOSE:     Creates a resolved issues mediawiki document for a release
# COPYRIGHT:   Copyright 2026 Carl Bialorucki <carl.bialorucki@reactos.org>
#

import sys
import unicodedata
import requests

JIRA_URL = "https://jira.reactos.org/rest/api/2/search"
MAX_SUMMARY_LENGTH = 100

def normalize_summary(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s if len(s) <= MAX_SUMMARY_LENGTH else s[:MAX_SUMMARY_LENGTH - 3] + "..."

def fetch_tickets(version):
    jql = f'fixVersion = "{version}"'

    # Largest valid maxResults value is 1000
    # See: https://developer.atlassian.com/cloud/jira/platform/change-notice-for-get-search-max-results
    params = {
        "jql": jql,
        "maxResults": 1000,
        "fields": "key,summary,issuetype"
    }

    response = requests.get(JIRA_URL, params=params)
    response.raise_for_status()
    data = response.json()
    return data["issues"]

def main():
    if len(sys.argv) < 2:
        print("Usage: python resolved-issues.py <version>")
        sys.exit(1)

    version = sys.argv[1]
    issues = fetch_tickets(version)

    groups = {
        "Bug Fixes": [],
        "Epics": [],
        "New Features": [],
        "Stories": [],
        "Tasks": [],
        "Improvements": [],
        "Sub-tasks": [],
    }

    for issue in issues:
        itype = issue["fields"]["issuetype"]["name"]

        if itype == "Bug":
            groups["Bug Fixes"].append(issue)
        elif itype == "Epic":
            groups["Epics"].append(issue)
        elif itype == "New Feature":
            groups["New Features"].append(issue)
        elif itype == "Story":
            groups["Stories"].append(issue)
        elif itype == "Task":
            groups["Tasks"].append(issue)
        elif itype == "Improvement":
            groups["Improvements"].append(issue)
        elif itype == "Sub-task":
            groups["Sub-tasks"].append(issue)

    for group_name, issues in groups.items():
        print(f"== {group_name} ==")
        if not issues:
            print("''No issues were resolved in this category.''")
            print()
            continue

        for issue in issues:
            key = issue["key"]
            summary = issue["fields"]["summary"]
            print(f"* [https://jira.reactos.org/browse/{key} <nowiki>{key}</nowiki>] {normalize_summary(summary)}")
        print()

if __name__ == "__main__":
    main()
