# 项目可观测性设计

本文件填写本项目的具体实现决策；通用规则以 [可观测性基线](../specs/observability.md) 为准。当前只是待填写设计，不是已经部署的采集体系。

## 负责人、覆盖范围与裁剪

{{OBS_OWNER_SCOPE_AND_EXCEPTIONS}}

列出服务、Worker、客户端、批处理等运行单元。逐项引用 OBS-001～OBS-010；不适用项写明理由、替代验证和批准记录，而不是直接删除要求。

## 信号管线与技术选型

{{OBS_PIPELINE_AND_SDK}}

记录 SDK/日志库及版本、语义约定版本、采集器、传输协议、存储与查询后端。说明本地/测试/生产差异、初始化和关闭入口、配置来源、网络权限与凭证管理。默认考虑 OpenTelemetry 兼容方案，但不强制特定后端。

## 资源身份与关联

{{OBS_RESOURCE_AND_CONTEXT_MAPPING}}

明确服务名、版本、环境字段映射，trace/span 与日志的关联方式，入口信任边界、异步传播与第三方外发白名单。

## 日志事件目录

| 稳定事件名 | 触发点/责任边界 | 级别 | 安全字段与类型 | 截断/脱敏 | 关联标识 |
| --- | --- | --- | --- | --- | --- |
| {{OBS_EVENT}} | {{OBS_TRIGGER}} | {{OBS_LEVEL}} | {{OBS_FIELDS}} | {{OBS_REDACTION}} | {{OBS_CORRELATION}} |

## 指标目录

| 指标 | 类型/单位 | 计数时机与分母 | 标签及允许值 | 序列预算/桶边界 | 对应规则 |
| --- | --- | --- | --- | --- | --- |
| {{OBS_METRIC}} | {{OBS_METRIC_TYPE_UNIT}} | {{OBS_COUNTING}} | {{OBS_LABELS}} | {{OBS_CARDINALITY_BUCKETS}} | {{OBS_RULES}} |

## Trace 边界与采样

{{OBS_SPANS_PROPAGATION_AND_SAMPLING}}

列出实际边界、span 名称及属性白名单、重试/并发/消息语义、采样率或策略、错误/慢链路保留限制和失去上下文时的行为。

## 容量、可靠性与隐私

{{OBS_BUDGETS_RELIABILITY_AND_PRIVACY}}

必须明确：日志级别及速率/大小限制、指标活跃序列预算、导出队列容量/超时/重试、flush 截止时间、存储保留期、访问/删除策略、性能开销上限及比较方法。说明观测系统自身故障的带外检测。

## SLI/SLO、查询与告警

{{OBS_SLOS_DASHBOARDS_ALERTS_AND_RUNBOOKS}}

填写真实指标查询、目标窗口/阈值/分母、无数据策略、仪表盘/告警配置位置及负责人，链接 `operations/runbooks/` 中的排障文档。配置尽可能版本化，不将访问令牌写入 URL。

## 验证入口

实际验收命令、场景状态与证据统一维护在 [可观测性验收清单](../tests/acceptance/observability.md)，避免复制后产生漂移。项目初始化时也要落实产品 CI 的必需检查。
