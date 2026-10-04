# {{FEATURE_NAME}}

- 功能 ID：{{FEATURE_ID}}
- 规格状态：草案
- 负责人：{{OWNER}}
- 批准记录：尚未批准

## 目标与非目标

{{GOALS_AND_NON_GOALS}}

## 用户场景

{{USER_SCENARIOS}}

## 业务规则

规则 ID 在项目内唯一且稳定；以下 ID 需替换为实际前缀。

- {{PREFIX}}-001：{{RULE}}

## 状态与数据变化

{{STATES_TRANSITIONS_INVARIANTS}}

## 权限、安全与隐私

{{PERMISSIONS_AND_DATA_PROTECTION}}

## 异常与边界

{{FAILURES_TIMEOUTS_RETRIES_CONCURRENCY}}

## 交互要求

{{NORMAL_LOADING_EMPTY_ERROR_STATES}}

## 契约与依赖

{{LINKS_TO_CONTRACTS_AND_DEPENDENCIES}}

引用权威契约，不复制接口字段定义。不适用时写明原因。

## 验收与追踪

| 规则 ID | 前提 Given | 操作 When | 结果 Then | 验证方式/测试位置 | 负责人 |
| --- | --- | --- | --- | --- | --- |
| {{PREFIX}}-001 | {{GIVEN}} | {{WHEN}} | {{THEN}} | {{VERIFICATION}} | {{OWNER}} |

## 风险与发布

{{COMPATIBILITY_MIGRATION_ROLLOUT_RECOVERY}}

## 待决问题

{{OPEN_QUESTIONS_OR_NONE}}
