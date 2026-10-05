# Engineering Template

以规格为中心、以验证为门禁的通用工程模板。不绑定语言、框架或部署平台，也不预置业务功能。

## 从这里开始

GitHub 可按以下步骤创建；GitLab 请使用下方的克隆方式。

1. 在 GitHub 仓库 Settings 中启用 **Template repository**。
2. 使用 **Use this template** 创建独立产品仓库。
3. 按 [初始化清单](docs/initialization.md) 填写产品目标、选择技术栈并配置权限。
4. 从 `docs/templates/feature-spec.md` 复制出 `docs/specs/<feature>.md`，审阅后实现第一个功能。
5. 每个行为变更在同一 PR 内同步规格、实现和验证证据。

### 在 GitLab 中使用

先在 GitLab 创建**空项目**，不要初始化 README、许可证或 `.gitignore`。然后执行：

```sh
# 1. 克隆模板；my-system 替换为你的项目名称
git clone https://github.com/pokitpeng/engineering-template.git my-system
cd my-system

# 2. 将 origin 改为实际 GitLab 项目地址
git remote set-url origin git@gitlab.com:YOUR_GROUP/my-system.git

# 3. 确认远程地址
git remote -v

# 4. 推送到 GitLab
git push -u origin main
```

如果使用 HTTPS，第 2 步改为：

```sh
git remote set-url origin https://gitlab.com/YOUR_GROUP/my-system.git
```

将 `YOUR_GROUP` 替换为实际命名空间（可包含子组）；自建 GitLab 还需替换域名。SSH 方式需配置 SSH 公钥，HTTPS 方式按实例要求使用访问令牌或凭证管理器，不要把令牌写入远程 URL。

这种方式**保留模板的提交历史**，不会自动同步模板更新。推送后继续按 [初始化清单](docs/initialization.md) 完成项目配置。

**注意：推送成功不代表 GitLab 工程约束已配置。** 当前模板的平台配置面向 GitHub，在 GitLab 中还需要适配：

| 当前配置 | GitLab 对应配置 |
| --- | --- |
| `.github/workflows/checks.yml` | 根目录 `.gitlab-ci.yml`，并配置可用 Runner |
| `.github/pull_request_template.md` | `.gitlab/merge_request_templates/Default.md` |
| `.github/CODEOWNERS` | `.gitlab/CODEOWNERS` |
| GitHub 分支保护与审批 | GitLab 受保护分支、合并检查与审批设置 |

`scripts/check_project.py` 目前要求 `.github/` 文件存在，且固定检查 `.github/CODEOWNERS`。迁移这些文件时，必须同步调整检查器及其测试；不能只移动目录。平台约束应在 GitLab 中单独配置，部分审批能力取决于版本和订阅等级。

## 目录与权威来源

| 路径 | 内容 |
| --- | --- |
| `docs/product/goals.md` | 用户、场景、目标、非目标 |
| `docs/product/capabilities.md` | 功能索引与交付状态；不重复业务规则 |
| `docs/product/glossary.md` | 业务术语 |
| `docs/specs/` | 业务规则、状态、交互、验收与规则 ID |
| `docs/architecture/overview.md` | 模块边界、技术选型、质量约束 |
| `docs/architecture/decisions/` | 重要决策的背景、取舍和后果 |
| `docs/specs/observability.md` | 默认继承的日志、指标、trace 规则 |
| `docs/architecture/observability.md` | 项目采集管线、信号目录、预算与监控设计 |
| `docs/operations/runbooks/` | 经验证的告警排查与恢复手册 |
| `docs/acceptance/` | 验收方案、人工验收记录与证据索引 |
| `contracts/api/`、`contracts/schemas/` | 接口与共享数据契约；不维护重复定义 |
| `tests/acceptance/` | 跨模块或跨系统的业务验收测试 |
| `docs/templates/` | 可重复使用的空白模板，不是实际规格 |
| `docs/README.md` | 文档导航、阅读顺序与组织约定 |
| `scripts/` | 可执行的通用检查及其测试 |
| `.github/` | PR 模板、负责人配置、CI |
| `AGENTS.md` | AI 工作协议；不是权限隔离机制 |

完整导航见 [文档中心](docs/README.md)。说明、规格与设计统一放在 `docs/`；根目录保留 `README.md`、`AGENTS.md` 作为入口。机器可读契约保留在 `contracts/`，可执行验收测试保留在 `tests/acceptance/`，两者不迁入文档目录。

源码目录由项目选定，可使用 `src/`，也可使用 `backend/` 和 `frontend/`。局部测试跟随源码，跨系统验收放 `tests/acceptance/`。不要为匹配目录而人为拆分业务。

## 开发闭环

需求与规则 → 审阅 → 实现与测试 → 提交验证证据 → 审批与合并 → 发布反馈。

详细约定见 [开发流程](docs/workflow.md)。高风险变更（权限、资金、删除、迁移等）先批准规格和风险方案；小变更可在同一 PR 内完成。

## 内置工程基线：可观测性

人可以提供目标，由 AI 起草规格、拆解任务和编码；但产物不能只交付功能代码。AI 的默认交付范围还包含可观测性、验证证据和排障方法，关键业务取舍及风险接受仍由负责人决定。

所有新项目继承 [OBS-001～OBS-010](docs/specs/observability.md)：

- **Logs**：结构化事件、统一身份、错误分类及 trace/span 关联。
- **Metrics**：吞吐、结果、延迟分布与饱和度，明确单位、分母和标签预算。
- **Traces**：关键跨边界调用及异步上下文，默认优先兼容 OpenTelemetry / W3C Trace Context。
- **可操作性**：查询、SLO、告警、runbook 和真实导出链路验收。
- **安全与成本**：脱敏、采样、保留期限、基数限制和采集故障隔离。不是默认全量记录所有输入、响应和变量。

落地顺序：填写 [项目可观测性设计](docs/architecture/observability.md) → 选择技术栈并实现 → 运行 [验收清单](docs/acceptance/observability.md) 对应测试 → 提交真实证据。每份功能规格和变更计划都包含可观测性增量要求。

**本模板提供规范、设计模板、流程约束和文档检查；没有预装 SDK、Collector、监控后端或运行时验收测试。** 新项目必须根据技术栈实现这些能力，并将真实检查接入 CI/发布流程。可观测性帮助定位运行时问题，但不能替代测试、代码审查与安全验证。

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

**这些检查只验证模板结构、指定目录内的本地 Markdown 文件链接，以及初始化占位符；不能证明业务正确、安全或运行时可观测性完成验收。** 严格模式会检查 `docs/product/`、`docs/architecture/`、`docs/specs/`、`docs/operations/`、`docs/acceptance/` 及 `tests/acceptance/` 中说明文件的占位符；空白 `docs/templates/` 不受影响。链接检查不验证网络链接、锚点、引用式链接或 HTML。模板检查的测试也不是产品测试。

## 模板版本与升级

当前源仓库：`https://github.com/pokitpeng/engineering-template`。
模板版本记录在 `TEMPLATE_VERSION`；版本标签需由维护者实际发布。

新项目保留此文件作为来源记录。模板创建的仓库不会自动同步上游变化；通过上游变更记录按需迁移流程和检查。不要覆盖项目自己的业务规格或决策。

## 已有约束与待配置约束

- 已提供：本地结构检查、检查器自测、GitHub Actions、PR 模板、可观测性基线与验收设计。
- 需项目实现/配置：埋点与采集管线、仪表盘/告警、真实测试、有效 CODEOWNERS、分支保护、必需检查、审批与环境权限。
- `AGENTS.md`、PR 勾选框和 CODEOWNERS 文件本身都不能强制阻止合并。

初始化后请将本 README 的项目说明替换为实际系统说明，并保留适用的流程与命令入口。
