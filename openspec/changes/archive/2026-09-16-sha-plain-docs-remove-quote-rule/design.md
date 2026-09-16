## Context

动机见 proposal.md。当前 `check_plain.py` 的 `check_punctuation` 内嵌 `quote_style` 检查块（`"|''` 命中报 violation）；规则表述散落在 `rules-zh.md`（authoritative）两处、`docs/rules.md`（展示副本）一处、主 spec 一处。规则源反转机制（commit 4ad3578）已删除 drift 脚本，`docs/rules.md` 允许滞后，但本次是规则删除，滞后会让展示副本保留已废止规则，故手动同步。

## Goals / Non-Goals

**Goals:**
- 删除引号风格约束：脚本不再报 `quote_style` violation；规则源与展示副本同步删除表述；主 spec 同步。
- 保留其余标点检查（半角改全角、中英文空格、数字标点空格）不受影响。

**Non-Goals:**
- 不调整 `avoid-words.md`（无引号词条）。
- 不触碰 `sha-plain-talk` 与归档 change 快照。
- 不做任何引号自动纠偏/规范化替代方案——用户明确删除该约束，非替换。

## Decisions

### D-1. 删除而非保留为 oxo 告警（失效于用户拍板）

**决定**：完全删除 `quote_style` 检查块及相关消息；同时删除 `check_plain.py` 中不再使用的引号正则。备选"降级为 warning/allowlist"被否决——用户明确"一点用也没有、可能误伤"，保留为告警仍会产生噪音。

### D-2. 展示副本同步删除（弱于规则源反转的"允许滞后"）

**决定**：`docs/rules.md` 手动同步删除引号表述。理由：允许滞后是为避免机械同步负担；但**已废止**规则留在展示副本会误导读者以为仍是约束。单向手动同步，不恢复 drift 机制。

### D-3. spec 同步为 MODIFIED 而非 REMOVED

**决定**：主 spec《目标语言选择》requirement 保留，删除句中"引号统一「」"约束，并新增边界 Scenario（"引号风格不构成违规"）。理由：需求能力本身（选定语言+应用规则）不变，只是约束集合缩小。

## Risks / Trade-offs

- **[误伤中文引号规范]** 删除后正文混用中西引号不再有机器提示 → 缓解：属用户接受的取舍（"对理解没有帮助"）；语义层 rubric 无引号项，评估不受影响。
- **[半角标点检查误伤]** `"` / `'` 本身不受 `HALFWIDTH_PUNCT`（`,.;:?!(`）覆盖，删除 quote_style 后 ASCII 引号完全放行 → 预期行为，与 D-1 一致。

## Migration Plan

1. 改 `check_plain.py`（删检查块）。
2. 改 `rules-zh.md`（两处）+ `docs/rules.md`（一处）+ 主 spec（一处）。
3. 验证：`openspec validate --specs`；`check_plain.py` 带引号用例回归（期望 0 violation）；其余检查（句长/禁词/来源/标点）不受影响。
4. archive（openspec archive）→ W4 单提交（change 目录 + 主 spec + 代码）。

## Open Questions

无。