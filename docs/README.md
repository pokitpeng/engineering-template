# 文档中心

产品意图、工程规则、设计决策与操作说明集中在本目录。反引号中的仓库路径默认相对于仓库根目录；Markdown 链接相对于所在文档。

## 推荐阅读顺序

1. [初始化清单](initialization.md)：从模板建立新项目。
2. [产品目标](product/goals.md)、[功能索引](product/capabilities.md)、[术语表](product/glossary.md)：明确做什么。
3. [开发流程](workflow.md)、[规格约定](specs/README.md)：明确如何变更和证明完成。
4. [架构概览](architecture/overview.md)、[决策记录](architecture/decisions/README.md)：明确实现边界与取舍。
5. [可观测性基线](specs/observability.md) → [项目设计](architecture/observability.md) → [验收清单](acceptance/observability.md)：落实日志、指标、trace 与证据。
6. [排障手册](operations/runbooks/README.md)：运行时定位与恢复。

## 文档模板

- [功能规格](templates/feature-spec.md)：复制到 `docs/specs/<feature>.md`。
- [变更计划](templates/change-plan.md)：用于复杂任务，可随 PR 提交或在 PR 中填写。
- [架构决策](templates/adr.md)：复制到 `docs/architecture/decisions/`。
- [排障手册](templates/runbook.md)：复制到 `docs/operations/runbooks/`。

空白模板可以保留占位符；复制后的项目文档需填写真实信息，不适用项说明原因。

## 与代码和工具的边界

- [验收文档](acceptance/README.md) 存放方案、人工记录与证据索引；[tests/acceptance](../tests/acceptance/README.md) 存放可执行验收测试。
- [API 契约](../contracts/api/README.md) 与 [共享数据格式](../contracts/schemas/README.md) 保留在根目录 `contracts/`，供校验或生成代码使用。
- [项目入口](../README.md) 与 [AI 工作协议](../AGENTS.md) 保留在根目录；`.github/` 保留平台配置，`scripts/` 保留自动化程序。
- 文档不重复手工维护契约、测试报告或配置中的事实，优先链接其权威来源。

## 从旧目录布局迁移

旧项目同步本次调整时，将根目录的 `product/`、`specs/`、`architecture/`、`templates/`、`operations/` 移入 `docs/`；将 `tests/acceptance/observability.md` 移至 `docs/acceptance/observability.md`，保留实际测试代码。

同时更新本项目自定义链接、AI 指令、CODEOWNERS、脚本和 CI 路径过滤器，不覆盖项目已有业务内容。新建模板项目无需重复迁移。
