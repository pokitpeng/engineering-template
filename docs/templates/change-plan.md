# {{CHANGE_TITLE}}

- 负责人：{{OWNER}}
- 关联规格与规则 ID：{{SPEC_AND_RULE_IDS}}
- 风险等级与理由：{{RISK}}

## 目的与范围

{{PURPOSE_SCOPE_NON_GOALS}}

## 必须保持不变的行为

{{INVARIANTS}}

## 受影响模块与契约

{{IMPACT}}

## 实施步骤

{{STEPS}}

任务拆解需覆盖业务逻辑、可观测性、测试与排障文档；不适用项说明理由。

## 可观测性影响

{{OBS_AFFECTED_RULES_EVENTS_METRICS_SPANS_AND_RUNBOOKS}}

引用适用 OBS 规则；说明新增/变化的采集字段、指标基数、采样、性能与数据保护风险，以及监控查询兼容性。

## 验证计划

{{AUTOMATED_AND_MANUAL_VERIFICATION}}

包括三类信号实际导出后的关联、合成失败、脱敏与导出故障隔离。部署侧告警验收与普通 CI 测试分别列明，未执行项不得预填通过。

## 兼容、迁移与回滚/恢复

{{RECOVERY_PLAN}}

## 待确认事项及批准证据

{{QUESTIONS_AND_APPROVAL}}

## 执行结果

实施后填写实际执行命令、结果与未完成项，不预填通过。
