# Engineering Template

以规格为中心、以验证为门禁的通用工程模板。不绑定语言、框架或部署平台，也不预置业务功能。

## 从这里开始

1. 在 GitHub 仓库 Settings 中启用 **Template repository**。
2. 使用 **Use this template** 创建独立产品仓库。
3. 按 [初始化清单](docs/initialization.md) 填写产品目标、选择技术栈并配置权限。
4. 从 `templates/feature-spec.md` 复制出 `specs/<feature>.md`，审阅后实现第一个功能。
5. 每个行为变更在同一 PR 内同步规格、实现和验证证据。

## 目录与权威来源

| 路径 | 内容 |
| --- | --- |
| `product/goals.md` | 用户、场景、目标、非目标 |
| `product/capabilities.md` | 功能索引与交付状态；不重复业务规则 |
| `product/glossary.md` | 业务术语 |
| `specs/` | 业务规则、状态、交互、验收与规则 ID |
| `architecture/overview.md` | 模块边界、技术选型、质量约束 |
| `architecture/decisions/` | 重要决策的背景、取舍和后果 |
| `contracts/api/`、`contracts/schemas/` | 接口与共享数据契约；不维护重复定义 |
| `tests/acceptance/` | 跨模块或跨系统的业务验收测试 |
| `templates/` | 可重复使用的空白模板，不是实际规格 |
| `docs/` | 开发流程、初始化说明 |
| `scripts/` | 可执行的通用检查及其测试 |
| `.github/` | PR 模板、负责人配置、CI |
| `AGENTS.md` | AI 工作协议；不是权限隔离机制 |

源码目录由项目选定，可使用 `src/`，也可使用 `backend/` 和 `frontend/`。局部测试跟随源码，跨系统验收放 `tests/acceptance/`。不要为匹配目录而人为拆分业务。

## 开发闭环

需求与规则 → 审阅 → 实现与测试 → 提交验证证据 → 审批与合并 → 发布反馈。

详细约定见 [开发流程](docs/workflow.md)。高风险变更（权限、资金、删除、迁移等）先批准规格和风险方案；小变更可在同一 PR 内完成。

## 运行模板检查

依赖 Python 3.11+，只使用标准库：

```sh
python3 scripts/check_project.py
python3 -m unittest discover -s scripts/tests -v
```

完成项目初始化后，额外执行：

```sh
python3 scripts/check_project.py --initialized
```

CI 默认执行前两项。完成初始化后应将 CI 检查命令加上 `--initialized`，并接入真实的类型检查、构建和测试。

**这些检查只验证模板结构、指定目录内的本地 Markdown 文件链接，以及初始化占位符；不能证明业务正确、安全或完成验收。** 链接检查不验证网络链接、锚点、引用式链接或 HTML。模板检查的测试也不是产品测试。

## 模板版本与升级

当前源仓库：`https://github.com/pokitpeng/engineering-template`。
模板版本记录在 `TEMPLATE_VERSION`；版本标签需由维护者实际发布。

新项目保留此文件作为来源记录。模板创建的仓库不会自动同步上游变化；通过上游变更记录按需迁移流程和检查。不要覆盖项目自己的业务规格或决策。

## 已有约束与待配置约束

- 已提供：本地结构检查、检查器自测、GitHub Actions、PR 模板。
- 需项目配置：实际测试、有效 CODEOWNERS、分支保护、必需检查、审批与环境权限。
- `AGENTS.md`、PR 勾选框和 CODEOWNERS 文件本身都不能强制阻止合并。

初始化后请将本 README 的项目说明替换为实际系统说明，并保留适用的流程与命令入口。
