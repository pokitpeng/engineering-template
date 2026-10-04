# 架构概览

## 技术栈与运行环境

{{STACK_AND_RUNTIME}}

## 源码布局与模块边界

{{MODULES_AND_DEPENDENCY_DIRECTION}}

局部测试跟随源码，跨系统业务验收放在 `tests/acceptance/`。不要求使用特定语言或目录名。

## 数据与契约

{{DATA_OWNERSHIP_AND_CONTRACT_SOURCE}}

确定契约权威来源、生成命令及生成产物位置；不适用的部分明确说明原因。

## 质量与安全约束

{{SECURITY_PERFORMANCE_AND_RELIABILITY}}

## 项目命令

填写可直接执行的真实命令；项目 CI 应调用同一入口。不适用的操作明确说明原因，不能以占位空命令假装检查通过。

| 操作 | 命令 |
| --- | --- |
| 安装 | {{INSTALL_COMMAND}} |
| 开发 | {{DEV_COMMAND}} |
| 构建 | {{BUILD_COMMAND}} |
| 静态检查 | {{CHECK_COMMAND}} |
| 测试 | {{TEST_COMMAND}} |
| 验收 | {{ACCEPTANCE_COMMAND}} |

## 部署与恢复

{{DEPLOYMENT_MIGRATIONS_AND_RECOVERY}}

重要取舍记录在 `architecture/decisions/`，使用 `templates/adr.md`。
