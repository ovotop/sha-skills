# Design: clause-too-long-warning

## Context

`check_plain.py:190` 把 `clause_too_long` 标为 violation（exit 1），但 `references/rules-zh.md:48` 写的是「尽量保持在 20 字以内」。软规则被硬脚本执行，写作者为过检删宾语。`CLAUSE_SPLIT = [，、]` 把每个逗号当子句边界，中文逗号也用于节奏/列举/固定短语内部，会误伤语义完整的 V-O 单元。整句 40 字上限不卡（加全宾语约 30 字），真正卡住的是构件 ≤20。

## Goals / Non-Goals

**Goals:**
- `clause_too_long` 与 rules-zh.md 的「尽量」对齐：warning，不计入 exit code
- message 明确「先改句式、禁止删信息」，阻断删宾语过检的反模式
- SKILL.md 工作流同步这条约束，agent 修订时不压过度

**Non-Goals:**
- 不改 40 字整句上限（仍 violation）
- 不删 `clause_too_long` 检查本身（压短解析单元的意图合理）
- 不做依存分析判断逗号是否真子句边界（P2，除非大量误报再开）
- 不加 `--strict` 开关（YAGNI，有团队需要硬门禁再加）

## Decisions

### 1. severity：violation → warning（而非保持 violation + 只改 message）

- **选择**：warning
- **理由**：message 改得再好，agent 看到 exit 1 仍会优先消 violation；只有降级才能真正解除「改到 0 violations」的压力。rules-zh.md 已写「尽量」，warning 是语义上唯一对齐的强度。
- **备选**：保持 violation + message 加指引 —— 治标不治本，agent 仍会为消红删信息。

### 2. message 措辞：强制改写指引 + 禁止删信息

```text
逗号构件 N 字（目标 ≤20）。优先改句式：拆句 / 去掉不必要逗号 / 缩短修饰。禁止为过检删除关键宾语、条件或否定。
```

- 不用「请拆分」这种弱指令 —— 它没传达优先级，agent 会用删信息来「拆分」。

### 3. rules-zh.md 不动

已写「尽量」，与 warning 对齐，无需改。`docs/rules.md` 是展示副本，允许滞后。

### 4. evals.json 不动

期望「构件 ≤20 字」是 LLM 评审核心规则用的（评输出质量），不依赖脚本 severity。降级后「没有 violation」反而更容易满足，不影响评分。

### 5. SKILL.md 两处同步

- 工作流第 5 步：加「构件超长先改句式，删事实属于违规不是解法；30–39 字 info 确认语义完整后可保留」
- 内核表句长条目：标注构件检查为 warning，提示勿删事实

## Risks / Trade-offs

- [warning 被 agent 忽略] → message 里写明「禁止删信息」，SKILL.md 工作流再压一层；30–40 字 info 仍存在，构件 warning 只是提示
- [CLAUSE_SPLIT 误伤仍在] → P2 后置，除非出现大量误报；当前务实默认是 P0+P1 够用
