# gh-pre

An experimental tool that helps with Project Release Engineering, focused on
repository clusters (groups of repositories which need to be released in
particular order).

```shell
gh extension install pycontribs/gh-pre
```

Usage:

```shell
gh pre
```

It can also be installed and executed as a Python package:

```shell
pip install gh-pre
pre
```

## Configuration

Please create a `~/pre.yml` config file with content similar to:

```
repos:
    - github-org/project1
    - github-org/project2
```

This will tell it which repositories to check for draft releases.
