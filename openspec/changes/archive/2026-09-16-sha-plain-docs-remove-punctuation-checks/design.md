## Context

承接 `sha-plain-docs-remove-quote-rule`（已归档）。动机见 proposal.md。当前 `check_punctuation` 剩余 3 个检查：`halfwidth_punctuation`（半角→全角）、`extra_space_before_punct`（数字与全角标点间空格）、`missing_cjk_latin_space`（中英混排空格）。用户拍板删除前两者（标点处理对理解无帮助且半角逗号会误伤源码），保留第三者。

规则源反转机制（commit 4ad3578）下 `docs/rules.md` 允许滞后，但规则删除需手动同步展示副本，避免读者误解已废止规则仍有效。

## Goals / Non-Goals

**Goals:**
- 删除全部标点符号检查：脚本不再报 `halfwidth_punctuation` / `extra_space_before_punct`；规则源与展示副本同步；主 spec 更新检查范围。
- 保留中英混排空格检查 `missing_cjk_latin_space`（排版可读性规则，非标点处理）。

**Non-Goals:**
- 不调整句长双层、check_facts、删改对比、avoid-words。
- 不触碰 `sha-plain-talk` 与归档快照。
- 不做任何标点自动纠偏/规范化的替代方案——用户明确删除该约束。

## Decisions

### D-1. 删除两类标点检查，保留中英空格（用户拍板）

**决定**：`check_punctuation` 只保留 `missing_cjk_latin_space`；删除 `halfwidth_punctuation` 检查块、`extra_space_before_punct` 检查块，及仅被二者使用的常量 `HALFWIDTH_PUNCT`、`FULLWIDTH_AFTER_DIGIT`。

**理由**：用户上一轮（引号）与本轮（标点）的决策逻辑一致——严格标点规则对理解无帮助。`missing_cjk_latin_space` 例外：`中文 与 英文123` 的混排空格是排版可读性规则，不构成对源码的误伤（不检查标点字符，只检查 CJK 与拉丁/数字之间是否需要空格）。

**备选**：
- 全部删除 `check_punctuation`（否决：丢失有实际价值的中英空格检查，用户未要求）。
- 保留 `halfwidth_punctuation` 但加代码段豁免（否决：mismatch 到"任何标点都不处理"的用户意图，豁免逻辑也难穷尽 `foo(a, b)` 这类内联场景）。

### D-2. mask_line 能力不变（源码片段继续规避其他检查）

**决定**：`mask_line` 对反引号代码段 / URL 的掩码机制保留。删除标点检查后，内联源码里即使反引号缺失也不再被标点规则误伤（本轮目标）；但黑话、句长等检查对掩码外的代码仍有行为——属既有设计，不动。

### D-3. 展示副本同步删除（同上一轮 D-2）

**决定**：`docs/rules.md`「标点一致」行手动同步为仅保留"中文与英文数字之间加空格"。单向手动同步，不恢复 drift 机制。

## Risks / Trade-offs

- **[中文排版风格回归]** 半角/全角混用不再有机器提示 → 缓解：用户接受的取舍（对理解无帮助且会误伤源码）；语义层 rubric 无标点项，评估不受影响。
- **[中英空格误伤]** `missing_cjk_latin_space` 保留，仍可能对 `中文ABC标识符` 之类边界报空格违规 → 缓解：该规则只涉及空格（排版）不涉及标点，语义明确；如后续误伤可单独收敛。

## Migration Plan

1. 改 `check_plain.py`：删两个检查块 + 两个常量。
2. 改 `rules-zh.md`（表格「标点一致」行 + 「混排与标点细则」条目）+ `docs/rules.md`（「标点一致」行）+ 主 spec（《目标语言选择》《确定性验证》）。
3. 验证：`openspec validate --specs`；`check_plain.py` 回归——`foo(a, b)`、`192.168.0.1`、`配置 maxConnections 为 200。` 期望 0 violation；中文与英文数字间缺空格样本仍报 `missing_cjk_latin_space`；黑话/句长行为不变。
4. archive（openspec archive）→ W4 单提交（change 目录 + 主 spec + 代码）。

## Open Questions

无。