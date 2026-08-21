# Engineering Agent Skills

面向软件工程调查、规划、审查、安全、运维和交付工作流的可移植、Provider 无关的 Agent Skills。

本仓库收录遵循开放 Agent Skills 规范、可被兼容编码 Agent 使用的独立 Skill。每个 Skill 自带工作流、配置模板、完全虚构的示例、机器可读评测、对抗性案例、评测标准，以及运行时可忽略的 Agent UI 元数据。

## 安装与快速开始

使用兼容的 Skill 安装工具，从 GitHub 安装单个 Skill：

```bash
npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill pr-mr-review
```

将 `pr-mr-review` 替换为下方目录中的任意 Skill 名称；需要时按安装工具支持的参数选择目标 Agent。安装后可显式调用：

```text
使用 pr-mr-review 审查这个 Pull Request，不要发表评论或审批。
```

若使用 GitHub Copilot，可将同一份可移植目录安装到其支持的 Agent 位置：

```bash
npx skills@1.5.20 add haoyuqi/engineering-agent-skills --skill pr-mr-review --agent github-copilot
```

仓库不维护 Copilot 专用副本；安装器负责选择运行时目录，通用 `SKILL.md` 始终是唯一事实来源。

Codex、Claude Code、OpenCode 和 GitHub Copilot 的已验证打包目录、手工复制方式及验证边界见[兼容性与安装说明](docs/compatibility.md)。

配置模板是显式提供给 Agent 的策略输入，既不是凭据存储，也不能隐式授权写操作。修改模板前请阅读已校验的[配置契约](docs/configuration-contract.md)。

`requirements-clarification` 的三种模式依赖以下两个外部安装的 Skill；本仓库不会打包它们：

- `obra/superpowers:brainstorming`：安装命令：`npx skills@1.5.20 add obra/superpowers --skill brainstorming`
- `mattpocock/skills:grill-me`：该上游包装 Skill 会调用 `mattpocock/skills:grilling`；应一起安装：`npx skills@1.5.20 add mattpocock/skills --skill grill-me --skill grilling`

本 Skill 不替代或额外规定这两个外部 Skill 的生命周期。用户选定的依赖缺失时，本 Skill 的流程会停止，且不会写入需求文档。

上述命令使用本仓库已验证的安装器固定版本。可以使用更新版本，但在重新运行兼容性测试并更新记录前，不属于已验证的打包范围。

## 开发披露

本仓库在 AI 协助下开发。编码 Agent 可参与 Skill 与文档的调研、起草、审阅、
测试和维护；维护者仍对范围、来源可追溯性、安全、测试及每一次发布决定负责。
未经审阅和验证，AI 输出不构成证据。

无论内容是否由 AI 协助产出，公开发布前都必须通过
[docs/privacy-review.md](docs/privacy-review.md) 所述的公开内容与来源复核。

## 校验本地检出

仓库提供离线结构和公开内容校验，检查官方元数据约束、每个已选 Skill 的资源、工作流与触发边界用例、链接和常见隐私风险；它不会安装依赖，也不会调用外部 Skill。

```bash
python3 tests/test_repository_structure.py
python3 tests/test_workflow_supply_chain.py
python3 tests/test_compatibility_contract.py
python3 tests/test_configuration_contract.py
python3 tests/test_public_content.py
python3 tests/test_public_content_coverage.py
python3 tests/test_public_content.py --history
python3 tests/test_repository_vulnerability_discovery.py
python3 tests/test_repository_vulnerability_normalization.py
python3 tests/test_repository_vulnerability_audit_runner.py
python3 tests/test_core_eval_fixtures.py
python3 tests/test_evaluation_contract.py
python3 tests/test_evaluation_result_validator.py
python3 tests/test_external_dependency_contract.py
python3 tests/test_template_quality.py
```

CI 还会使用固定版本 `skills@1.5.20` 运行联网打包测试，将全部 Skill 安装到 Codex、Claude Code、OpenCode 和 GitHub Copilot 的代表性项目目录，并逐文件对比资源。测试带有超时限制，npm 不可用时会明确失败而不会一直挂起。仅在可访问 npm 时本地运行：

```bash
python3 tests/test_installer_compatibility.py
```

## 原则

- **仓库内独立**：每个 Skill 都是自包含目录，不依赖本仓库中的其他 Skill；如有外部依赖，会在该 Skill 的文档中明确声明。
- **Provider 无关**：GitHub、GitLab、本地 Git、需求管理工具和安全扫描器均为可选输入，不是硬依赖。
- **默认只读**：评论、审批、提交、推送及外部更新均需用户明确确认。
- **证据优先**：每项发现必须关联 diff、文件位置、需求、依赖版本或工具输出；未知信息必须明确标注。
- **可验证**：每个 Skill 都包含脱敏示例和离线评测用例。

本仓库的完整质量门槛见 [docs/skill-quality-standard.zh-CN.md](docs/skill-quality-standard.zh-CN.md)。[docs/design-benchmarks.md](docs/design-benchmarks.md) 记录采用的上游机制和有意保留的差异；[docs/privacy-review.md](docs/privacy-review.md) 定义公开内容的自动脱敏与人工来源复核门槛。

[docs/evaluation.md](docs/evaluation.md) 说明触发测试、基于 fixture 的工作流评测、
重复运行记录，以及“离线结构通过”和“模型行为已验证”之间的区别。模型运行证据
只有在基于已提交的 Skill 版本复现，并按[结果格式](docs/evaluation-result-format.md)
校验后才可发布。

## 已包含的 Skill

| Skill | 功能 |
| --- | --- |
| [deep-build](skills/deep-build/) | 规划、实现、验证并独立审查大型改动，在 Git 交付前停止。 |
| [git-change-delivery](skills/git-change-delivery/) | 通过逐步确认完成暂存、提交、推送和 GitHub PR/GitLab MR。 |
| [pr-mr-review](skills/pr-mr-review/) | 对照需求和代码审查 GitHub PR、GitLab MR 或本地补丁。 |
| [repository-vulnerabilities](skills/repository-vulnerabilities/) | 自动发现并审计当前代码库的 Composer/npm 锁文件。 |
| [requirements-clarification](skills/requirements-clarification/) | 通过外部探索与压力测试，将当前讨论整理为可测试需求草案。 |

## 许可证

采用 [Apache License 2.0](LICENSE)。
