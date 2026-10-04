# 项目初始化清单

模板内容使用 `{{PLACEHOLDER}}` 标记需要替换的位置。`templates/` 内的占位符应保留供未来复制。

## 产品与规格

- [ ] 填写 `product/goals.md` 中的用户、场景、目标、非目标和负责人。
- [ ] 建立项目术语表；功能索引只记录已确认的功能。
- [ ] 从功能模板创建第一份规格，分配稳定规则 ID，明确未决问题。
- [ ] 关键规则有验证方法；不能自动化的部分有人工验收负责人。

## 技术与命令

- [ ] 填写 `architecture/overview.md`，确定源码布局、技术栈、模块边界。
- [ ] 写清并实际运行安装、启动、构建、检查、测试命令。
- [ ] 接入产品测试；不得以模板检查替代业务验证。
- [ ] 选择是否需要契约生成；确定权威来源，避免多份手工维护。
- [ ] 替换 README 为项目使用说明，保留模板来源与版本记录。

## 可观测性（所有新项目默认继承）

- [ ] 阅读 [OBS 基线](../specs/observability.md)，在 [项目设计](../architecture/observability.md) 填写采集管线、SDK、资源身份与上下文策略。
- [ ] 实现统一日志、指标和 trace 初始化/关闭；按实际运行形态覆盖关键边界，不适用项有理由及批准。
- [ ] 填写事件/指标目录、标签白名单、采样、队列/导出超时、开销预算、数据保留和访问策略。
- [ ] 创建实际仪表盘、告警与 `operations/runbooks/` 手册，明确负责人及无数据/采集故障检测。
- [ ] 按 [可观测性验收清单](../tests/acceptance/observability.md) 实现并运行测试，填写命令、CI job 与真实证据；模板 CI 不代替运行时验收。

## GitHub 与安全（需要平台配置）

- [ ] 用实际有仓库访问权限的用户或团队替换 `.github/CODEOWNERS` 中的注释示例，确认 GitHub 能识别。
- [ ] 启用 Actions；加入本项目检查和测试 job。
- [ ] 将模板检查命令改为 `python3 scripts/check_project.py --initialized`。
- [ ] 为默认分支配置规则集或分支保护：通过 PR 合并、必需检查、必要审批，并限制绕过权限。
- [ ] 如需负责人审批，单独启用 Require review from Code Owners。
- [ ] 单人项目明确自审的局限；不要假装已具备独立审批。
- [ ] 配置最小权限凭证、环境审批和部署边界；不在仓库保存秘密。
- [ ] 决定项目许可证（模板未预设许可证）。

## 完成验证

```sh
python3 scripts/check_project.py --initialized
python3 -m unittest discover -s scripts/tests -v
```

严格模式额外检查 `product/`、`architecture/`、`specs/`、`operations/` 和 `tests/acceptance/` 文档占位符以及 CODEOWNERS 是否存在活动规则，不校验文字质量、运行时可观测性、用户权限或平台保护配置。上面的检查清单仍需负责人实际确认。
