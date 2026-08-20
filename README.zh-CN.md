# Engineering Agent Skills

面向软件工程规划与交付工作流的可移植、Provider 无关的 Agent Skills。

本仓库收录遵循开放 `SKILL.md` 约定、可被兼容编码 Agent 使用的独立 Skill。当前聚焦于将模糊的产品或工程讨论整理为可审阅的需求草案。

## 安装与快速开始

使用兼容的 Skill 安装工具，从本地检出目录安装单个 Skill：

```bash
npx skills add ./engineering-agent-skills --skill requirements-clarification -a codex
```

将 `codex` 替换为安装工具支持的目标 Agent。安装后可显式调用：

```text
使用 requirements-clarification，将当前讨论整理为可测试的需求草案。
```

`requirements-clarification` 的三种模式依赖以下两个外部安装的 Skill；本仓库不会打包它们：

- `obra/superpowers:brainstorming`：来自 `obra/superpowers`，安装命令：`npx skills add https://github.com/obra/superpowers --skill brainstorming`
- `mattpocock/skills:grill-me`：来自 `mattpocock/skills`，安装命令：`npx skills add https://github.com/mattpocock/skills --skill grill-me`

本 Skill 不替代或额外规定这两个外部 Skill 的生命周期。用户选定的依赖缺失时，本 Skill 的流程会停止，且不会写入需求文档。

## 校验本地检出

仓库提供离线结构校验，检查必要文档、每个 Skill 的资源和 `SKILL.md` 元数据；它不会安装依赖，也不会调用外部 Skill。

```bash
python3 tests/test_repository_structure.py
```

## 原则

- **仓库内独立**：每个 Skill 都是自包含目录，不依赖本仓库中的其他 Skill；如有外部依赖，会在该 Skill 的文档中明确声明。
- **Provider 无关**：GitHub、GitLab、本地 Git、需求管理工具和安全扫描器均为可选输入，不是硬依赖。
- **默认只读**：评论、审批、提交、推送及外部更新均需用户明确确认。
- **证据优先**：每项发现必须关联 diff、文件位置、需求、依赖版本或工具输出；未知信息必须明确标注。
- **可验证**：每个 Skill 都包含脱敏示例和离线评测用例。

## 已包含的 Skill

| Skill | 功能 |
| --- | --- |
| [requirements-clarification](skills/requirements-clarification/) | 通过外部探索与压力测试流程，将当前讨论整理为可测试的需求草案。包含[完全虚构的输入/输出示例](skills/requirements-clarification/examples/input-output.md)和离线评测用例。 |
| [repository-vulnerabilities](skills/repository-vulnerabilities/) | 审计 Composer/npm 锁文件；注册表访问、确定性证据汇总和外部漏洞库核验均设有明确确认边界。 |
| [deep-build](skills/deep-build/) | 通过书面 Plan、独立审阅门禁和证据化交接实施大型改动，在 Git 交付前停止。 |

## 许可证

采用 [Apache License 2.0](LICENSE)。
