# StoryOS 设计草案

## 目标

做一个比传统“提示词写小说”更可靠的长篇创作系统：

- 长篇不崩设定
- 审计可编程
- 状态能回滚/比对
- 后续可接多模型与 UI

## 核心流水线

1. **Plan**：确定本章目标、冲突、节拍、状态变更意图
2. **Draft**：基于 plan + state 生成正文
3. **Audit**：规则检查 + LLM 审查
4. **Revise**：按审计结果返修
5. **Apply**：将状态变更提交到世界状态

## 比 InkOS 更想强化的点

### 1. 规则引擎优先
明显错误不该浪费 LLM：
- 角色未注册
- 资源不存在
- 伏笔状态冲突
- 时间线倒退
- 场景位移冲突

### 2. 状态为结构化事实，不是提示词附件
后续可以支持：
- state diff
- 图谱分析
- 角色视角信息边界
- 自动生成 recap

### 3. 风格模块独立
风格不和连续性审计混在一起：
- continuity
- prose quality
- anti-ai-style
- genre constraints

## 下一阶段任务

- draft 命令
- apply 命令
- 角色/资源/伏笔增删改命令
- JSON Schema 校验
- 测试集与 benchmark
