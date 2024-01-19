"""Expose features related to git repositories."""
from __future__ import annotations
import json

import datetime
from subprocess import run

from rich.panel import Panel
from rich import box
from rich.console import Console


def main() -> None:
    """Main entrypoint."""
    console = Console()
    repos = [
        "ansible/ansible-compat",
        "ansible/ansible-lint",
        "ansible/ansible-navigator",
        "ansible/ansible-creator",
        "ansible/molecule",
        "ansible/tox-ansible",
        "ansible/pytest-ansible",
        "ansible/ansible-development-environment",
        "ansible/ansible-dev-tools",
        "ansible/creator-ee",
    ]
    for repo in repos:
        repo_link = f"[markdown.link][link=https://github.com/{repo}]{repo}[/][/]"
        result = run(
            f'gh api repos/{repo}/releases --jq "[.[] | select(.draft)"]',
            text=True,
            shell=True,
            capture_output=True,
            check=True,
        )
        drafts = json.loads(result.stdout)
        if not drafts or (
            isinstance(drafts, dict) and drafts["message"] == "Not Found"
        ):
            console.print(f"🟢 {repo_link} [dim]has no draft release.[/]")
            continue
        for draft in drafts:
            created = datetime.datetime.fromisoformat(draft["created_at"]).replace(
                tzinfo=None
            )
            age = (datetime.datetime.now() - created).days
            if not draft["body"].strip():
                console.print(f"🟢 {repo_link} [dim]has an empty draft release.[/]")
                continue

            md = Panel(draft["body"].replace("\n\n", "\n").strip("\n"), box=box.MINIMAL)
            msg = (
                f"🟠 {repo_link} draft release "
                + f"[link={draft['html_url']}][markdown.link]{draft['tag_name']}[/][/]"
                + f" created [repr.number]{age}[/] days ago:\n"
            )
            console.print(msg, highlight=False, end="")
            console.print(md, style="dim")


if __name__ == "__main__":
    # execute only if run as a script
    main()
