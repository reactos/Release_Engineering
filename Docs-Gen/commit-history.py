#
# PROJECT:     ReactOS Release Document Scripts
# LICENSE:     MIT (https://spdx.org/licenses/MIT)
# PURPOSE:     Creates a commit history mediawiki document for a release
# COPYRIGHT:   Copyright 2026 Carl Bialorucki <carl.bialorucki@reactos.org>
#

import subprocess
import sys
import re
import unicodedata
from collections import defaultdict

MISC_TITLE = "Miscellaneous"
MAX_MSG_LENGTH = 100
skip_prefixes = []

class Commit:
    def __init__(self, sha, author, message):
        self.sha = sha
        # Normalize and strip author, message
        self.author = unicodedata.normalize("NFKD", author.strip()).encode("ascii", "ignore").decode("ascii")
        self.message = unicodedata.normalize("NFKD", message.strip()).encode("ascii", "ignore").decode("ascii")

def truncate_msg(s):
    return s if len(s) <= MAX_MSG_LENGTH else s[:MAX_MSG_LENGTH - 3] + "..."

def run(cmd):
    return subprocess.run(cmd, text=True, capture_output=True, encoding="utf-8").stdout.strip()

def parse_message_prefix(msg):
    # Skip over some prefixes
    for prefix in skip_prefixes:
        if msg.startswith(f"[{prefix}]"):
            msg = msg[msg.find("]") + 1:].lstrip()

    match = re.match(r"\[([^\]:]+)(?::([^\]]+))?\]", msg)
    if match:
        group = match.group(1).upper()
        subgroup = match.group(2) or None
        return group, subgroup
    return MISC_TITLE, None

def main():
    if len(sys.argv) < 2:
        print("Usage: python commit-history.py <parent_branch>")
        sys.exit(1)

    parent = sys.argv[1]
    branch = run("git rev-parse --abbrev-ref HEAD")
    raw_commits = run(f'git log {parent}..{branch} --pretty=format:"%h|%an|%s" --reverse').split("\n")
    current_version = branch.split("releases/", 1)[1]
    # Add current version as a skipped prefix
    skip_prefixes.append(current_version)

    # groups[group][subgroup] = list of commits
    groups = defaultdict(lambda: defaultdict(list))

    for entry in raw_commits:
        if not entry.strip():
            continue

        sha, author, message = entry.split("|", 2)
        commit = Commit(sha, author, message)
        group, subgroup = parse_message_prefix(commit.message)
        groups[group][subgroup].append(commit)

    print(f"''Note: commits prefixed with the version number (i.e. [{current_version}]) are specific to this release. Backported commits from after the release was branched will also have this prefix.''\n")
    # All properly formatted commits first, then misc
    for group in sorted(groups.keys(), key=lambda g: (g == MISC_TITLE, g)):
        print(f"== {group} ==")
        # None subgroup first, then alphabetical
        for subgroup in sorted(groups[group].keys(), key=lambda x: (x is not None, x or "")):
            if subgroup is not None:
                print(f"=== {subgroup} ===")

            for commit in groups[group][subgroup]:
                print(f"* [https://git.reactos.org/?p=reactos.git;a=commit;h={commit.sha} <nowiki>{truncate_msg(commit.message)}</nowiki>] ({commit.author})")

            print()

if __name__ == "__main__":
    main()
