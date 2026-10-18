# Proposal: clause-too-long-warning

## Why

`check_plain.py` 把「逗号构件 ≤20 字」标为 violation（exit 1），但权威规则 `references/rules-zh.md` 写的是「**尽量**保持在 20 字以内」——软规则被硬脚本执行。写作者（含 agent）看到 lint fail 会优先改到 0 violations，在「改句式 vs 删信息」之间选择删宾语过检，导致文档句子缺宾语、条件被删（2026-10-08 实测复现：「在平台两个环境变量里各加一条 jobCode 映射即可」加回宾语后构件 25 字被打成 violation，删宾语才过检）。

## What Changes

- `check_plain.py`：`clause_too_long` severity 从 **violation** 降为 **warning**（不计入 exit code），与 rules-zh.md 的「尽量」对齐
- `check_plain.py`：`clause_too_long` 的 message 改为强制改写指引——优先改句式（拆句/去不必要逗号/缩修饰），**禁止为过检删除关键宾语、条件或否定**
- `SKILL.md`：工作流「跑脚本」步骤增加约束——构件超长先改句式，删事实属于违规不是解法；30–39 字 info 确认语义完整后可保留
- `SKILL.md`：内核表「句长[zh]」标注构件检查为 warning，并提示勿删事实

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `sha-plain-docs`：确定性验证需求变更——`clause_too_long` 从硬性违规降为告警，message 从「请拆分」改为「优先改句式、禁止删信息」；工作流新增「删事实不是解法」约束。

## Impact

- `skills/sha-plain-docs/scripts/check_plain.py`：L190 severity + message
- `skills/sha-plain-docs/SKILL.md`：工作流第 5 步 + 内核表句长条目
- 不改 `references/rules-zh.md`（已写「尽量」，无需动）
- 不改 `docs/rules.md`（展示副本，允许滞后）
- 不改 `evals/evals.json`（期望「构件 ≤20 字」是评审核心规则用的，不依赖脚本 severity）
- 不改 40 字整句上限（仍 violation）
- 不删 `clause_too_long` 检查本身
