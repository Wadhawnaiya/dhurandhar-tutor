# Contributing to Dhurandhar Tutor

**English** | [简体中文](CONTRIBUTING_CN.md)

Thanks for helping build Dhurandhar! Code, docs, translations, bug reports and
answering other people's questions all count as contributions.

Community: [Discussions](https://github.com/Wadhawnaiya/dhurandhar-tutor/discussions) ·
[Issues](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues)

- [Where to start](#where-to-start)
- [Pull requests](#pull-requests)
- [Development setup](#development-setup)

---

## Where to start

| You have | Do this |
| --- | --- |
| A bug | Open a [bug report](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=bug_report.yml) with steps to reproduce, your version and OS. Small, obvious fixes can go straight to a PR. |
| A feature or behavior change | Open a [feature request](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=feature_request.yml) first and wait for a maintainer to agree on the direction before writing code. |
| A docs or translation problem | Open a [docs issue](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=docs.yml) or send a PR. |
| A question or setup trouble | Ask in [Discussions](https://github.com/Wadhawnaiya/dhurandhar-tutor/discussions). |
| A security vulnerability | Report it privately through [GitHub security advisories](https://github.com/Wadhawnaiya/dhurandhar-tutor/security/advisories/new). Never open a public issue. |

Looking for something to work on? Try issues labeled
[`good first issue`](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
or [`help wanted`](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22),
and leave a comment so others know you're on it.

---

## Pull requests

**Target `dev`.** `main` only moves at a release, and PRs opened against it
are retargeted before review.

- **One change per PR.** Don't mix unrelated fixes, formatting or refactors.
- **Link the issue** with `Closes #123` or `Related to #123`.
- **Explain the problem and show evidence.** Say what was wrong and what
  changed, then show it works: test output, a screenshot or recording for UI
  changes, or logs.
- **Run the checks** that fit your change (see [Testing](docs-for-dev/TESTING.md)),
  plus `pre-commit run --all-files`. CI runs the full suite.
- **Leave "Allow edits by maintainers" on** so we can push small fixes and get
  your PR merged faster.
- **AI-assisted PRs are welcome.** No label needed, but you must understand
  the code you submit and include evidence, like any other PR.

We usually don't accept:

- Refactor-only PRs, unless a maintainer asked for one.
- Large features that weren't discussed in an issue first.
- More than 20 open PRs from one author at a time. Finish some before opening more.

### Commit messages

```
<type>: <short description>
```

`feat` new feature · `fix` bug fix · `docs` documentation · `refactor` no
behavior change · `test` tests · `chore` build, tooling or dependencies

---

## Development setup

The [developer handbook](docs-for-dev/README.md) is the source of truth:
[Agent setup](docs-for-dev/AGENT_SETUP.md) for installation and configuration,
[Development](docs-for-dev/DEVELOPMENT.md) for the source workflow and
[Architecture](docs-for-dev/ARCHITECTURE.md) for where code lives. The short version
(Python 3.11–3.14, Node.js 22 LTS):

```bash
git clone https://github.com/<you>/Dhurandhar.git && cd Dhurandhar
git checkout dev

python -m pip install -r requirements/full.txt
python -m pip install -e . --no-deps
python scripts/install_extras.py dev
(cd web && npm ci --legacy-peer-deps)

pre-commit install
```

Then branch from `dev` (`git checkout -b fix/short-name`). Keep build outputs,
runtime data and `node_modules` out of Git.
