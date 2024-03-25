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


class TyperApp(typer.Typer):
    """Our App."""

    repos: list[str]


app = TyperApp()
console = Console()


@app.callback(invoke_without_command=True)
@use_yaml_config(
    default_value=os.path.expanduser("~/pre.yml"),
    param_help="Configuration file (~/pre.yml).",
)
def default(repos: Annotated[Optional[list[str]], typer.Option()] = None) -> None:
    """Implicit entry point."""
    if repos is None:
        repos = []
    app.repos = repos


@app.command()
def main() -> None:
    """Pre helps you chain releases on github."""
    for repo in app.repos:
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


@app.command()
def prs() -> None:
    """List pending pull-request."""
    # for user in TEAM:
    # --review-requested=@{user}
    # --owner=ansible --owner=ansible-community
    cmd = (
        "GH_PAGER= gh search prs --draft=false --state=open --limit=100 --sort=updated"
    )
    cmd += "".join(f" --repo={repo}" for repo in app.repos)
    cmd += (
        " --template '{{range .}}{{tablerow .repository.nameWithOwner (timeago .updatedAt) "
        '.title (hyperlink .url (printf "#%v" .number) ) }}{{end}}{{tablerender}}\' '
        "--json title,url,repository,updatedAt,number"
    )
    console.print(f"[dim]{cmd}[/]", highlight=False)
    os.system(cmd)


@app.command()
def alerts() -> None:
    """List open alerts."""
    for repo in app.repos:
        cmd = "GH_PAGER= gh "
        cmd += f"api /repos/{repo}/dependabot/alerts"
        cmd += " --jq='.[] | select(.state!=\"fixed\") | .html_url'"
        result = run(
            cmd,
            text=True,
            shell=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            console.print(
                f"[dim]{cmd}[/dim] failed with {result.returncode}\n"
                f"{result.stdout}\n\n{result.stderr}"
            )
        else:
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(result.stderr)


if __name__ == "__main__":
    # execute only if run as a script
    app()
