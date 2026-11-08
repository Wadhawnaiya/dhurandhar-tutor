# 参与贡献 Dhurandhar Tutor

[English](CONTRIBUTING.md) | **简体中文**

感谢你参与 Dhurandhar 的建设！写代码、改文档、做翻译、报告 bug、回答别人的问题，都是贡献。

社区：[Discussions](https://github.com/Wadhawnaiya/dhurandhar-tutor/discussions) ·
[Issues](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues)

- [从哪里开始](#从哪里开始)
- [Pull Request](#pull-request)
- [开发环境](#开发环境)

---

## 从哪里开始

| 你遇到的情况 | 怎么做 |
| --- | --- |
| 发现 bug | 提交 [bug report](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=bug_report.yml)，写清复现步骤、版本和操作系统。小而明显的修复可以直接提 PR。 |
| 想加功能或改变行为 | 先提交 [feature request](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=feature_request.yml)，等 Maintainer 认可方向后再写代码。 |
| 文档或翻译有问题 | 提交 [docs issue](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues/new?template=docs.yml) 或直接提 PR。 |
| 有疑问或安装遇到问题 | 到 [Discussions](https://github.com/Wadhawnaiya/dhurandhar-tutor/discussions) 提问。 |
| 发现安全漏洞 | 通过 [GitHub security advisories](https://github.com/Wadhawnaiya/dhurandhar-tutor/security/advisories/new) 私下报告，不要公开提 issue。 |

想找点事做？可以看看带
[`good first issue`](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
或 [`help wanted`](https://github.com/Wadhawnaiya/dhurandhar-tutor/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
标签的 issue，并留言告诉大家你在做。

---

## Pull Request

**目标分支选 `dev`。** `main` 只在发版时更新，提到 `main` 的 PR 会先被改到 `dev` 再审核。

- **一个 PR 只做一件事。** 不要混入无关的修复、格式调整或重构。
- **关联 issue**，写上 `Closes #123` 或 `Related to #123`。
- **说明问题并给出证据。** 说清楚原来哪里有问题、改了什么，再证明它有效：测试输出、UI 改动的截图或录屏，或者日志。
- **运行与改动相关的检查**（见 [Testing](docs-for-dev/TESTING.md)），以及 `pre-commit run --all-files`。CI 会跑完整测试。
- **保持勾选 "Allow edits by maintainers"**，方便我们推送小修改，让你的 PR 更快合并。
- **欢迎用 AI 辅助写的 PR。** 不需要额外标注，但你必须理解自己提交的代码，并和其他 PR 一样附上证据。

我们一般不接受：

- 纯重构的 PR，除非是 Maintainer 要求的。
- 没有先在 issue 里讨论过的大功能。
- 同一作者同时开超过 20 个 PR。请先完成一些再开新的。

### Commit 信息

```
<type>: <short description>
```

`feat` 新功能 · `fix` 修复 bug · `docs` 文档 · `refactor` 不改变行为的重构 · `test` 测试 · `chore` 构建、工具或依赖

---

## 开发环境

以[开发者手册](docs-for-dev/README.md)为准：安装和配置看 [Agent setup](docs-for-dev/AGENT_SETUP.md)，源码开发流程看 [Development](docs-for-dev/DEVELOPMENT.md)，代码结构看 [Architecture](docs-for-dev/ARCHITECTURE.md)。简要步骤如下（Python 3.11–3.14，Node.js 22 LTS）：

```bash
git clone https://github.com/<you>/Dhurandhar.git && cd Dhurandhar
git checkout dev

python -m pip install -r requirements/full.txt
python -m pip install -e . --no-deps
python scripts/install_extras.py dev
(cd web && npm ci --legacy-peer-deps)

pre-commit install
```

然后从 `dev` 拉分支（`git checkout -b fix/short-name`）。不要把构建产物、运行时数据和 `node_modules` 提交到 Git。
