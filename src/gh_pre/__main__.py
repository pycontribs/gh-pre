"""Expose features related to git repositories."""
from __future__ import annotations
import json

import datetime
from subprocess import run
import os
from typing import Optional
from typing_extensions import Annotated

from rich.panel import Panel
from rich import box
from rich.console import Console
import typer
from typer_config.decorators import use_yaml_config


app = typer.Typer()


@app.command()
@use_yaml_config(
    default_value=os.path.expanduser("~/pre.yml"),
    param_help="Configuration file (~/pre.yml).",
)
def main(repos: Annotated[Optional[list[str]], typer.Option()] = None) -> None:
    """Pre helps you chain releases on github."""
    if repos is None:
        repos = []
    console = Console()
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
    app()
