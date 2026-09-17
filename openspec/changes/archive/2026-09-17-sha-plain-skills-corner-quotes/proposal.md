## Why

简体中文正文系统性误用直角引号「」『』——直角引号是日文标点与繁体竖排风格，用在简体中文里呈"日文感"。根源之一是本技能的规则与示范语料长期以「」标引用，模型输出随之沿用；2026-09-16 曾删除「引号统一「」」约束（remove-quote-rule：旧约束**强制**直角引号且误伤 ASCII 引号，删除方向正确），但规则与语料中的直角引号残留未清，输出仍带日文感。本次改为**反向约束**：简体中文正文必须用弯引号 " "，直角引号列为违规；ASCII 直引号维持豁免，不重蹈 remove-quote-rule 的误伤覆辙。

## What Changes

- **新增检出**：`check_plain.py` 对 zh 文档将直角引号「」『』报告为 `corner_quotes_in_zh` violation；code span / URL / 表格 / frontmatter 沿用现有跳过逻辑；ASCII 直引号不检查。
- **规则源**：`rules-zh.md`（权威源）标点与格式表新增「引号规范」行——简体中文用弯引号，不用直角引号；`docs/rules.md`（展示副本）同步。
- **spec 修订**：`sha-plain-docs`《目标语言选择》《确定性验证》引号表述改为"简体中文正文 MUST 用弯引号、直角引号违规、ASCII 直引号豁免"，新增/修订边界 Scenario；`sha-plain-talk`《微观规则》补同款通用规则（简体中文输出同约束）。
- **语料清扫**（仅规则与模型可见文件，非历史记录）：两个 SKILL.md、README、change delta spec、trigger-queries 的「」→弯引号；`check_plain.py` 内部诊断消息同步自洽。**不动**：`docs/evals.md` 历史段落、`skills/*/evals/*` 夹具、`openspec/changes/archive/` 快照。
- **行为变更**：zh 文档含直角引号时 `check_plain.py` 退出码 1（violation）。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `sha-plain-docs`: 《目标语言选择》与《确定性验证》——简体中文正文禁用直角引号、强制弯引号，ASCII 直引号豁免保留。
- `sha-plain-talk`: 《微观规则》——新增简体中文引号规范（用弯引号，不用直角引号，适用重讲输出）。

## Impact

- `skills/sha-plain-docs/scripts/check_plain.py`（新增检查块 + 消息自洽）
- `skills/sha-plain-docs/references/rules-zh.md`（权威源）+ `docs/rules.md`（展示副本）
- `openspec/specs/sha-plain-docs/spec.md`、`openspec/specs/sha-plain-talk/spec.md`（主 spec，经 archive 合并）
- 两个 SKILL.md、README.md、`skills/sha-plain-talk/evals/trigger-queries.json`（语料清扫）
- 兼容性：与 remove-quote-rule 的 ASCII 直引号豁免正交，不冲突；不触碰 archive 快照与历史记录。