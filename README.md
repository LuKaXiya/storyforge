# StoryOS

StoryOS 是一个面向长篇小说创作的工程化写作系统原型。

它受 InkOS 启发，但目标不是简单复刻，而是强化这几件事：

- **结构化状态管理**：世界状态、角色、资源、伏笔使用 JSON 持久化
- **可编程审计**：连续性检查先走规则引擎，再交给 LLM 做风格和创作增强
- **流水线清晰**：计划 → 草稿 → 审计 → 修订 → 状态提交
- **易扩展**：后续可接入任意 LLM、Web UI、数据库、协作工作流

> 目前版本是 MVP 原型，重点验证项目结构、状态模型、章节规划与规则审计能力。

## 当前能力

### 1. 初始化小说项目
```bash
python3 storyos.py init demo-book --title "赛博修仙" --genre "都市修仙"
```

生成：
- `story.json`：书籍元信息
- `state/world.json`：世界状态
- `state/characters.json`：角色清单与记忆边界
- `state/resources.json`：资源账本
- `state/hooks.json`：伏笔/承诺
- `chapters/`：章节目录
- `plans/`：章节计划
- `audits/`：审计报告
- `drafts/`：草稿

### 2. 生成章节计划
```bash
python3 storyos.py plan demo-book --goal "主角第一次发现灵气复苏" --conflict "要不要暴露能力"
```

输出结构化 plan，包含：
- 本章目标
- 冲突
- 场景 beat 列表
- 状态变更建议
- 应新增/回收伏笔

### 3. 审计章节
```bash
python3 storyos.py audit demo-book --chapter 1 --text-file sample_ch1.txt
```

当前内置规则：
- 未知角色提及
- 已关闭伏笔再次当作未揭示内容引用
- 消耗不存在的资源
- 明显重复句检测
- 过量总结句式提示

### 4. 查看项目状态
```bash
python3 storyos.py status demo-book
```

## 为什么说它有机会做得比 InkOS 更好

不是今天就比它全，而是架构上更适合继续往前做：

1. **规则审计和 LLM 审计分层**
   - 可确定的问题交给代码
   - 模糊问题交给 LLM
   - 减少纯 prompt 幻觉

2. **状态模型可验证**
   - 角色、资源、伏笔是可枚举实体
   - 后续可以做 diff、回滚、图谱分析

3. **更适合产品化**
   - 后续可接 API / Web UI / 多人协作 / Git 版本管理

4. **更适合你的长期使用**
   - 可以做成你自己的中文网文写作系统，而不是照搬别人 CLI

## 目录结构

```text
story-os/
├── storyos.py
├── storyos/
│   ├── __init__.py
│   ├── models.py
│   ├── planner.py
│   ├── auditor.py
│   ├── storage.py
│   └── templates.py
└── README.md
```

## 下一步建议

- 接入 LLM：让 `plan` / `draft` / `revise` 真正联动模型
- 增加 `draft` 命令：按 plan 自动生成章节草稿
- 增加 `apply` 命令：审计通过后把状态变更正式提交到 world/resources/hooks
- 增加 `style` 子系统：抽取文风指纹，约束生成
- 增加 `canon import`：导入既有文本进行续写

## 快速演示

```bash
python3 storyos.py init demo-book --title "赛博修仙" --genre "都市修仙"
python3 storyos.py plan demo-book --goal "主角在地铁里第一次感知灵气" --conflict "是否当场出手救人"
python3 storyos.py status demo-book
```

如果你愿意，下一步我可以继续把它扩成：
- 真正可写章节的版本
- 支持续写/同人/仿写的版本
- 带 Web UI 的版本
