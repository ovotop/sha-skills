## Why

中文正文「引号统一用「」」这条规则对用户理解内容没有任何帮助，反而可能误伤正文（如直接引用英文原文、代码注释、翻译稿中的 ASCII 引号），产生无价值的违规报告。用户明确拍板删除：这不是重复规则，而是"一点用也没有"，还带误伤风险。

## What Changes

- 删除 `check_plain.py` 的 `quote_style` 检查（ASCII 直引号 `"` / `''` 不再报 violation）。
- 从 `references/rules-zh.md` 删除两处引号规则表述：表格「标点一致」行中"引号统一「」"部分，以及「混排与标点细则」中"中文引号统一用「」；中文正文不使用 " " 或 " "。"整条。
- 从 `docs/rules.md`（展示副本）同步删除「标点一致」行中引号部分。
- 主 spec `openspec/specs/sha-plain-docs/spec.md`《目标语言选择》requirement 中删除"引号统一「」"表述。
- **保留**其余标点规则不变：半角标点改全角（`halfwidth_punctuation`）、中英文/数字间空格、数字与全角标点间无空格。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

- `sha-plain-docs`: 《目标语言选择》requirement 删除"引号统一「」"约束；《确定性验证》项 1 的标点检查范围不再包含引号风格。

## Impact

- `skills/sha-plain-docs/scripts/check_plain.py`（删 `quote_style` 检查块 + 常量引用清理）
- `skills/sha-plain-docs/references/rules-zh.md`（authoritative 规则源）
- `docs/rules.md`（展示副本，同步删除）
- `openspec/specs/sha-plain-docs/spec.md`（主 spec 同步）
- 不触碰：`sha-plain-talk`、归档 change 快照、check_facts / 句长 / 断行逻辑