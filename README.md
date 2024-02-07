# gh-pre

An experimental tool that helps with Project Release Engineering, focused on
repository clusters (groups of repositories that need to be released in
particular order).

```shell
gh extension install pycontribs/gh-pre
```

## Configuration

To use the tool you need to configure the list of repositories it needs to check on each run:

```yaml
# ~/pre.yml
repos:
  - ansible/ansible-compat
  - ansible/ansible-lint
  - ansible/ansible-navigator
  - ansible/ansible-creator
  - ansible/molecule
  - ansible/tox-ansible
  - ansible/pytest-ansible
  - ansible/ansible-development-environment
  - ansible/ansible-dev-tools
  - ansible/creator-ee
```

This will tell it which repositories to check for draft releases.

## Usage

```shell
gh pre
```

It can also be installed and executed as a Python package:

```shell
pip install gh-pre
pre
```
